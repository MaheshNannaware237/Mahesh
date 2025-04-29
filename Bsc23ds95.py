# gym_ledger_app.py

import hashlib
import time
import streamlit as st

# Function to generate a unique hash for each ledger entry
def generate_hash(entry):
    entry_string = f"{entry['entry_no']}{entry['member_action']}{entry['timestamp']}{entry['previous_hash']}"
    return hashlib.sha256(entry_string.encode()).hexdigest()

# Function to create a new ledger entry
def create_ledger_entry(entry_no, member_action, previous_hash):
    return {
        "entry_no": entry_no,
        "member_action": member_action,
        "timestamp": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
        "previous_hash": previous_hash
    }

# Initialize the ledger with a genesis entry (only once)
if 'ledger' not in st.session_state:
    genesis_entry = create_ledger_entry(0, "Genesis Entry - Gym Ledger Start", "0")
    st.session_state.ledger = [genesis_entry]

# Function to add a new entry to the ledger
def add_ledger_entry(member_action):
    previous_entry = st.session_state.ledger[-1]
    new_entry_no = previous_entry["entry_no"] + 1
    new_hash = generate_hash(previous_entry)
    
    new_entry = create_ledger_entry(new_entry_no, member_action, new_hash)
    st.session_state.ledger.append(new_entry)

# Streamlit UI
st.title("🏋️‍♂️ Gym Membership Ledger")

st.subheader("📥 Add New Member Activity")
with st.form("ledger_form"):
    action_input = st.text_input("Enter member action (e.g., 'Member D - Joined Monthly Plan')", "")
    submitted = st.form_submit_button("Add to Ledger")
    if submitted and action_input.strip():
        add_ledger_entry(action_input.strip())
        st.success("Entry added to ledger!")

st.subheader("📜 Ledger Entries")
for entry in reversed(st.session_state.ledger):  # Show latest first
    st.write(f"**Entry #{entry['entry_no']}**")
    st.write(f"- Action: {entry['member_action']}")
    st.write(f"- Timestamp: {entry['timestamp']}")
    st.write(f"- Previous Hash: `{entry['previous_hash']}`")
    st.markdown("---")
