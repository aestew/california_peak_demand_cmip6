# requirements.txt:
# streamlit>=1.34.0
# boto3
# requests
# htbuilder

import streamlit as st
import requests
import boto3
import uuid
import time
import json
import os
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
from htbuilder.units import rem
from htbuilder import div, styles

# -----------------------------------------------------------------------------
# 1 CONFIG - I'm assuming we're setting these tables for each use case/function of the agent

# API & AWS Config
LLM_ENDPOINT = os.getenv("LLM_ENDPOINT", "http://localhost:8000/v1/chat/completions")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

# Resource Names
HISTORY_TABLE = os.getenv("HISTORY_TABLE", "FILL")
PREDICTIVE_TABLE = os.getenv("PREDICTIVE_TABLE", "FILL")
CACHE_TABLE = os.getenv("RESEARCH_TABLE", "FILL") 
S3_BUCKET_NAME = os.getenv("S3_BUCKET", "my-research-docs")

st.set_page_config(page_title="Wattson", page_icon="⚡️", layout="wide")

# -----------------------------------------------------------------------------
# 2 AWS CONNECTIONS

@st.cache_resource
def get_aws_resources():
    dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
    s3 = boto3.client("s3", region_name="us-east-1")
    return {
        "history": dynamodb.Table(HISTORY_TABLE),
        "predictive": dynamodb.Table(PREDICTIVE_TABLE),
        "cache": dynamodb.Table(CACHE_TABLE),
        "s3": s3
    }

aws = get_aws_resources()

# -----------------------------------------------------------------------------
# 3 ROUTER LOGIC

def decide_intent(user_query):
    """
    Classify the user's intent.
    Returns: 'PREDICTIVE' or 'INFORMATIVE'
    """
    system_prompt = (
        "You are a query classifier. "
        "If the user asks for forecasts, numbers, stats, or future predictions, reply 'PREDICTIVE'. "
        "If the user asks for definitions, concepts, how-to, or general info, reply 'INFORMATIVE'. "
        "Reply with ONLY one word."
    )
    
    payload = {
        "model": "custom-model",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_query}
        ],
        "temperature": 0.1, # low temp for strict classification
        "stream": False
    }

    try:
        # short time out for router since this should be fast
        resp = requests.post(LLM_ENDPOINT, json=payload, timeout=5)
        resp.raise_for_status()
        result = resp.json()['choices'][0]['message']['content'].strip().upper()
        
        if "PREDICTIVE" in result: return "PREDICTIVE"
        return "INFORMATIVE"
    except Exception as e:
        print(f"Router Error: {e}")
        return "INFORMATIVE" # Fallback

# -----------------------------------------------------------------------------
# 4 FETCH DATA

def get_predictive_data(query):
    """Queries the predictive results table from dynamodb."""
    table = aws["predictive"]
    try:
        response = table.scan(Limit=5)
        items = response.get('Items', [])
        return json.dumps(items, indent=2)
    except ClientError as e:
        return f"Database Error: {e}"

def get_research_data(query):
    """
    Simulates fetching documents?? or pulls from LLM response
    """
    # Query DynamoDB? OR we can switch to S3 Vector
    table = aws["research"]
    try:
        response = table.scan(Limit=3)
        items = response.get('Items', [])
        
        # Format the data for the LLM
        context_text = ""
        for item in items:
            title = item.get('title', 'Unknown Doc')
            body = item.get('content', 'No content')
            context_text += f"SOURCE: {title}\nCONTENT: {body}\n\n"
            
        return context_text
    except ClientError as e:
        return f"Research Error: {e}"

# -----------------------------------------------------------------------------
# 5 CHAT ENGINE

def get_llm_stream(messages):
    """Connects to RAG LLM endpoint from ECS"""
    clean_msgs = [{"role": m["role"], "content": m["content"]} for m in messages]
    
    payload = {
        "model": "custom-model",
        "messages": clean_msgs,
        "stream": True,
        "temperature": 0.7
    }
    
    try:
        with requests.post(LLM_ENDPOINT, json=payload, stream=True, timeout=60) as r:
            r.raise_for_status()
            for line in r.iter_lines():
                if line:
                    decoded = line.decode('utf-8')
                    if decoded.startswith("data: ") and decoded != "data: [DONE]":
                        try:
                            json_data = json.loads(decoded[6:])
                            chunk = json_data['choices'][0]['delta'].get('content', '')
                            if chunk: yield chunk
                        except: pass
    except Exception as e:
        yield f"**Connection Error:** {e}"

# -----------------------------------------------------------------------------
# 6 UI & CHAT

# Sidebar
with st.sidebar:
    # st.title("Navigation")
    # if st.button("Home", use_container_width=True): st.rerun()
    # if st.button("About Team", use_container_width=True): st.switch_page("pages/about_team.py")
    
    # st.divider()
    st.markdown("### System Status")
    st.success("ECS Cluster: Online")
    st.success("DynamoDB: Connected")

    st.markdown("### Available Features")
    st.caption("Energy Demand Model 1.0")
    st.caption("GoruRAG 1.0")

# Main Page
st.html(div(style=styles(font_size=rem(4), line_height=1))["🤖"])
st.title("Wattson 1.0")
st.caption("Electric Demand Research Assistant for California Grid Planning")

# Session State & History
if "session_id" not in st.session_state:
    st.session_state["session_id"] = str(uuid.uuid4())
    # Load history from DynamoDB
    try:
        h_resp = aws["history"].query(KeyConditionExpression=Key('session_id').eq(st.session_state.session_id))
        st.session_state.messages = h_resp.get('Items', [])
    except:
        st.session_state.messages = []

# Display Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# *** MAIN INTERACTION LOOP HERE!!! ***
if prompt := st.chat_input("Ask about energy forecasts or general research..."):
    
    # 1 Show User Message
    with st.chat_message("user"):
        st.text(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # 2 Process Response
    with st.chat_message("assistant"):
        response_container = st.empty()
        
        # 2A ROUTING STEP
        with st.status("Thinking...", expanded=True) as status:
            st.write("Analyzing intent...")
            intent = decide_intent(prompt)
            st.info(f"Classified as: **{intent}**")
            
            # 2B FETCHING STEP
            context_data = ""
            if intent == "PREDICTIVE":
                st.write("Calculating Predictions...")
                context_data = get_predictive_data(prompt)
                system_instruction = "You are a Data Analyst. Interpret the provided JSON data to answer the user."
            else:
                st.write("Searching Documents...")
                context_data = get_research_data(prompt)
                system_instruction = "You are a Researcher. Use the provided document snippets to explain the topic."
            
            status.update(label="Data Retrieved", state="complete", expanded=False)

        # 2C GENERATION STEP???
        augmented_message = f"""
        [CONTEXT BEGIN]
        {context_data}
        [CONTEXT END]
        
        User Question: {prompt}
        """
        
        # System + History + Current Augmented Prompt (for llm full context)
        llm_messages = [{"role": "system", "content": system_instruction}]
        # Last 5 messages of convo hist (excluding the current input)
        llm_messages.extend(st.session_state.messages[:-1][-5:])
        # Add current user input with augmented context
        llm_messages.append({"role": "user", "content": augmented_message})
        
        # Stream result
        full_response = st.write_stream(get_llm_stream(llm_messages))
    
    # 3 Cache to DynamoDB
    # Currently saves only simple prompts but not the entire context blob
    try:
        aws["history"].put_item(Item={'session_id': st.session_state.session_id, 'timestamp': timestamp, 'role': 'user', 'content': prompt})
        aws["history"].put_item(Item={'session_id': st.session_state.session_id, 'timestamp': timestamp+1, 'role': 'assistant', 'content': full_response})
    except Exception as e:
        st.error(f"Failed to save history: {e}")
        
    st.session_state.messages.append({"role": "assistant", "content": full_response})