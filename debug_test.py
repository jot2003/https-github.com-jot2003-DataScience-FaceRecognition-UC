import streamlit as st

def test_debug():
    st.warning("🔍 DEBUG TEST: This function was called")
    st.info("🔍 DEBUG TEST: Streamlit messages work here")
    return True

# Test the function
if st.button("Test Debug"):
    result = test_debug()
    if result:
        st.success("✅ Debug test completed") 