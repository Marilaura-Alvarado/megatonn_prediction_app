# -----------------------------
# Developer feedback chatbot
# -----------------------------
st.markdown(f'<div class="section-title">{T["feedback_title"]}</div>', unsafe_allow_html=True)

st.markdown(
    f"""
    <div class="note-card">
        {T["feedback_intro"]}
    </div>
    """,
    unsafe_allow_html=True
)

if len(st.session_state.feedback_messages) == 0:
    st.session_state.feedback_messages.append(
        {"role": "assistant", "content": T["feedback_welcome"]}
    )

for message in st.session_state.feedback_messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

feedback_prompt = st.chat_input(T["feedback_placeholder"])

if feedback_prompt:
    st.session_state.feedback_messages.append(
        {"role": "user", "content": feedback_prompt}
    )

    save_developer_feedback(feedback_prompt)

    st.session_state.feedback_messages.append(
        {"role": "assistant", "content": T["feedback_ack"]}
    )

    st.rerun()

if os.path.exists(FEEDBACK_FILE):
    with open(FEEDBACK_FILE, "rb") as feedback_file:
        st.download_button(
            label=T["download_feedback"],
            data=feedback_file,
            file_name="developer_feedback.csv",
            mime="text/csv"
        )
