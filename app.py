import streamlit as st
import pandas as pd
import re

st.set_page_config(
    page_title="NLP Text Annotation",
    page_icon="📝",
    layout="wide"
)

st.markdown("""
<style>
.main {
    background-color: #f8fafc;
}

.block-container {
    max-width: 1100px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

.title {
    font-size: 38px;
    font-weight: 700;
    color: #1e293b;
}

.subtitle {
    color: #64748b;
    font-size: 16px;
    margin-bottom: 25px;
}

.section-title {
    font-size: 22px;
    font-weight: 600;
    color: #1e293b;
    margin-top: 25px;
    margin-bottom: 12px;
}

.metric-box {
    background-color: white;
    padding: 20px;
    border-radius: 10px;
    border: 1px solid #e2e8f0;
    text-align: center;
}

.metric-title {
    color: #64748b;
    font-size: 13px;
}

.metric-value {
    color: #1e293b;
    font-size: 25px;
    font-weight: 700;
    margin-top: 5px;
}

.entity {
    background-color: #f1f5f9;
    padding: 8px 12px;
    border-radius: 6px;
    margin: 5px 0;
    color: #334155;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="title">Customer Support Text Annotation</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">NLP-based text annotation and quality checking system</div>',
    unsafe_allow_html=True
)

file_path = "data/annotated_messages.csv"
data = pd.read_csv(file_path)

if "analyzed" not in st.session_state:
    st.session_state.analyzed = False

if "message" not in st.session_state:
    st.session_state.message = ""

if "entities" not in st.session_state:
    st.session_state.entities = []

st.markdown(
    '<div class="section-title">Analyze Customer Message</div>',
    unsafe_allow_html=True
)

message = st.text_area(
    "Customer Message",
    value=st.session_state.message,
    placeholder="Example: My phone is broken and I need help immediately.",
    height=130
)

if st.button("Analyze Message", use_container_width=True):

    if message:

        text = message.lower()

        if "refund" in text or "money back" in text:
            suggested_intent = "REFUND_REQUEST"
        elif "payment" in text or "charged" in text:
            suggested_intent = "PAYMENT_ISSUE"
        elif "password" in text or "login" in text or "account" in text:
            suggested_intent = "ACCOUNT_ISSUE"
        elif "delivery" in text or "arrive" in text or "late" in text or "track" in text:
            suggested_intent = "DELIVERY_ISSUE"
        elif (
            "broken" in text
            or "damaged" in text
            or "phone" in text
            or "laptop" in text
            or "headphones" in text
            or "tablet" in text
            or "watch" in text
        ):
            suggested_intent = "PRODUCT_ISSUE"
        else:
            suggested_intent = "GENERAL_QUERY"

        if (
            "good" in text
            or "great" in text
            or "happy" in text
            or "excellent" in text
        ):
            suggested_sentiment = "POSITIVE"
        elif (
            "bad" in text
            or "angry" in text
            or "unhappy" in text
            or "disappointed" in text
        ):
            suggested_sentiment = "NEGATIVE"
        else:
            suggested_sentiment = "NEUTRAL"

        if (
            "urgent" in text
            or "immediately" in text
            or "as soon as possible" in text
        ):
            suggested_priority = "HIGH"
        elif "soon" in text or "problem" in text or "issue" in text:
            suggested_priority = "MEDIUM"
        else:
            suggested_priority = "LOW"

        entities = []

        order_id = re.findall(r"#\w+", message)

        if order_id:
            entities.append("ORDER_ID: " + order_id[0])

        amount = re.findall(
            r"₹\s?\d+(?:,\d+)*(?:\.\d+)?",
            message
        )

        if amount:
            entities.append("AMOUNT: " + amount[0])

        locations = [
            "Chennai",
            "Coimbatore",
            "Bangalore",
            "Mumbai",
            "Delhi"
        ]

        for location in locations:
            if location.lower() in text:
                entities.append("LOCATION: " + location)

        products = [
            "phone",
            "laptop",
            "headphones",
            "tablet",
            "watch"
        ]

        for product in products:
            if product in text:
                entities.append("PRODUCT: " + product)

        st.session_state.message = message
        st.session_state.entities = entities
        st.session_state.analyzed = True

        st.session_state.suggested_intent = suggested_intent
        st.session_state.suggested_sentiment = suggested_sentiment
        st.session_state.suggested_priority = suggested_priority

    else:
        st.warning("Please enter a customer message.")


if st.session_state.analyzed:

    st.markdown(
        '<div class="section-title">Analysis Result</div>',
        unsafe_allow_html=True
    )

    st.info(
        "Review the suggested annotations and change them if required."
    )

    intents = [
        "GENERAL_QUERY",
        "DELIVERY_ISSUE",
        "PAYMENT_ISSUE",
        "ACCOUNT_ISSUE",
        "PRODUCT_ISSUE",
        "REFUND_REQUEST"
    ]

    sentiments = [
        "POSITIVE",
        "NEUTRAL",
        "NEGATIVE"
    ]

    priorities = [
        "LOW",
        "MEDIUM",
        "HIGH"
    ]

    col1, col2, col3 = st.columns(3)

    with col1:
        intent = st.selectbox(
            "Intent",
            intents,
            index=intents.index(
                st.session_state.suggested_intent
            )
        )

    with col2:
        sentiment = st.selectbox(
            "Sentiment",
            sentiments,
            index=sentiments.index(
                st.session_state.suggested_sentiment
            )
        )

    with col3:
        priority = st.selectbox(
            "Priority",
            priorities,
            index=priorities.index(
                st.session_state.suggested_priority
            )
        )

    st.session_state.suggested_intent = intent
    st.session_state.suggested_sentiment = sentiment
    st.session_state.suggested_priority = priority

    st.markdown("**Entities**")

    if st.session_state.entities:

        for entity in st.session_state.entities:
            st.markdown(
                f'<div class="entity">{entity}</div>',
                unsafe_allow_html=True
            )

    else:
        st.info("No entities found.")

    if st.button("Save Annotation", use_container_width=True):

        new_row = {
            "Message": st.session_state.message,
            "Intent": st.session_state.suggested_intent,
            "Sentiment": st.session_state.suggested_sentiment,
            "Priority": st.session_state.suggested_priority,
            "Entities": ", ".join(st.session_state.entities)
        }

        data = pd.concat(
            [data, pd.DataFrame([new_row])],
            ignore_index=True
        )

        data.to_csv(file_path, index=False)

        st.success("Annotation saved successfully.")

        st.session_state.analyzed = False
        st.session_state.message = ""
        st.session_state.entities = []

        st.rerun()


st.markdown(
    '<div class="section-title">Annotated Dataset</div>',
    unsafe_allow_html=True
)

data = pd.read_csv(file_path)

st.dataframe(
    data,
    use_container_width=True,
    hide_index=True
)


st.markdown(
    '<div class="section-title">Quality Check</div>',
    unsafe_allow_html=True
)

passed = 0
failed = 0

with st.expander("View annotation quality checks"):

    for index, row in data.iterrows():

        text = row["Message"].lower()
        expected_intent = row["Intent"]

        if expected_intent == "REFUND_REQUEST":
            correct = "refund" in text or "money back" in text

        elif expected_intent == "DELIVERY_ISSUE":
            correct = (
                "delivery" in text
                or "arrive" in text
                or "late" in text
                or "track" in text
            )

        elif expected_intent == "PAYMENT_ISSUE":
            correct = "payment" in text or "charged" in text

        elif expected_intent == "ACCOUNT_ISSUE":
            correct = (
                "password" in text
                or "login" in text
                or "account" in text
            )

        elif expected_intent == "PRODUCT_ISSUE":
            correct = (
                "broken" in text
                or "damaged" in text
                or "product" in text
                or "phone" in text
                or "laptop" in text
                or "headphones" in text
                or "tablet" in text
                or "watch" in text
            )

        else:
            correct = True

        if correct:
            passed += 1
            st.success(f"Row {index + 1}: PASS")
        else:
            failed += 1
            st.error(f"Row {index + 1}: FAIL")


total = passed + failed
quality = (passed / total) * 100


st.markdown(
    '<div class="section-title">Quality Summary</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        f"""
        <div class="metric-box">
            <div class="metric-title">Total Records</div>
            <div class="metric-value">{total}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div class="metric-box">
            <div class="metric-title">Passed</div>
            <div class="metric-value">{passed}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f"""
        <div class="metric-box">
            <div class="metric-title">Failed</div>
            <div class="metric-value">{failed}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        f"""
        <div class="metric-box">
            <div class="metric-title">Quality Score</div>
            <div class="metric-value">{quality:.0f}%</div>
        </div>
        """,
        unsafe_allow_html=True
    )


st.markdown(
    '<div class="section-title">Annotation Dashboard</div>',
    unsafe_allow_html=True
)

intent_counts = data["Intent"].value_counts()

st.write(f"**Total Messages:** {len(data)}")

dashboard_columns = st.columns(3)

for index, (intent, count) in enumerate(intent_counts.items()):

    with dashboard_columns[index % 3]:

        st.markdown(
            f"""
            <div class="metric-box">
                <div class="metric-title">{intent}</div>
                <div class="metric-value">{count}</div>
            </div>
            """,
            unsafe_allow_html=True
        )