import streamlit as st
import json
import pandas as pd

st.set_page_config(page_title="Cloud Copilot", layout="wide")

st.title("☁️ AI Cloud Security Copilot")
st.markdown("### 🚀 Intelligent Risk & Cost Optimization Dashboard")

# Sidebar
st.sidebar.title("⚙️ Navigation")
option = st.sidebar.selectbox(
    "Choose View",
    ["Dashboard", "Insights", "Summary"]
)

uploaded_file = st.file_uploader("Upload Cloud Logs (JSON)", type="json")

if uploaded_file:

    try:
        data = json.load(uploaded_file)
        if not isinstance(data, list):
            st.error("Invalid format: JSON must be a list")
            st.stop()
    except:
        st.error("Invalid JSON file")
        st.stop()

    total_risks = 0
    total_cost_issues = 0
    savings = 0

    for server in data:
        if server.get("public_access", False):
            total_risks += 1
        if server.get("cpu_usage", 0) < 10:
            total_cost_issues += 1
            savings += server.get("monthly_cost", 0) // 2

    # DASHBOARD
    if option == "Dashboard":

        col1, col2, col3 = st.columns(3)
        col1.metric("🔐 Security Risks", total_risks)
        col2.metric("💰 Cost Issues", total_cost_issues)
        col3.metric("💵 Estimated Savings ($)", savings)

        risk_score = total_risks * 5 + total_cost_issues * 3
        st.metric("⚡ Risk Score", risk_score)

        st.markdown("---")

        st.subheader("📊 Visualization")

        df = pd.DataFrame({
            "Category": ["Security Risks", "Cost Issues"],
            "Count": [total_risks, total_cost_issues]
        })

        st.bar_chart(df.set_index("Category"))

        st.markdown("---")

        st.subheader("🚨 High Priority Alerts")

        for server in data:
            instance = server.get("instance_id", "Unknown")

            if server.get("public_access", False):
                st.error(f"🔴 HIGH RISK: {instance} is publicly accessible")

            elif server.get("cpu_usage", 0) < 10:
                st.warning(f"🟡 MEDIUM RISK: {instance} underutilized")

        st.markdown("---")

        st.subheader("🤖 AI Recommendations")

        for server in data:
            instance = server.get("instance_id", "Unknown")

            if server.get("public_access", False) or server.get("cpu_usage", 0) < 10:
                st.success(f"""
                **Instance {instance}**

                - Restrict public access  
                - Optimize resource size  
                - Estimated Savings: ${server.get("monthly_cost",0)//2}/month  

                💡 This creates both security and cost risks.
                """)

    # INSIGHTS
    elif option == "Insights":

        st.subheader("🧠 AI Insight Summary")

        for server in data:
            instance = server.get("instance_id", "Unknown")

            if server.get("public_access", False) or server.get("cpu_usage", 0) < 10:
                st.info(f"""
                Instance {instance} has misconfiguration.
                This may lead to security vulnerabilities and unnecessary costs.
                Optimization is recommended.
                """)

    # SUMMARY
    elif option == "Summary":

        st.subheader("📊 Summary Report")

        st.write(f"Total Servers: {len(data)}")
        st.write(f"Security Risks: {total_risks}")
        st.write(f"Cost Issues: {total_cost_issues}")
        st.write(f"Estimated Savings: ${savings}")

        # Download report
        report = {
            "Total Servers": len(data),
            "Security Risks": total_risks,
            "Cost Issues": total_cost_issues,
            "Estimated Savings": savings
        }

        st.download_button(
            label="📥 Download Report",
            data=json.dumps(report, indent=2),
            file_name="cloud_report.json",
            mime="application/json"
        )

        st.markdown("---")

        st.subheader("🎯 Why This Matters")

        st.write("""
        ✔ Reduces cloud cost  
        ✔ Improves security posture  
        ✔ Focuses only on important alerts  
        ✔ Helps faster decision making  
        """)