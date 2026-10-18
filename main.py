import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Dashboard | Analytics",
    page_icon="📊",
    layout="wide",
)

COLORS = ["#5B6CFF", "#16B8A6", "#FF9F43", "#F45B8D", "#8A63D2"]

st.markdown(
    """
    <style>
    .stApp {
        background:
            radial-gradient(ellipse at 8% 0%, rgba(91, 108, 255, 0.09), transparent 32%),
            #f5f7fc;
        color: #202944;
    }
    [data-testid="stHeader"] { background: rgba(245, 247, 252, 0.9); }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ffffff 0%, #f0f3ff 100%);
        border-right: 1px solid #e7eaf3;
    }
    .block-container { padding-top: 2rem; padding-bottom: 3rem; max-width: 1440px; }
    .hero {
        padding: 1.7rem 2rem;
        border: 1px solid #e3e8ff;
        border-radius: 22px;
        background: linear-gradient(110deg, #ffffff 0%, #eef1ff 58%, #e7fbf7 100%);
        box-shadow: 0 12px 35px rgba(57, 72, 130, 0.07);
        margin-bottom: 1.5rem;
    }
    .eyebrow {
        color: #5869dc;
        font-size: 0.75rem;
        font-weight: 750;
        letter-spacing: 0.14em;
        text-transform: uppercase;
    }
    .hero h1 { margin: 0.4rem 0 0.25rem; font-size: 2.2rem; color: #202944; }
    .hero p { margin: 0; color: #68738b; font-size: 1rem; }
    [data-testid="stMetric"] {
        padding: 1rem 1.15rem;
        border: 1px solid #e8ebf4;
        border-radius: 17px;
        background: #ffffff;
        box-shadow: 0 5px 18px rgba(57, 72, 130, 0.045);
    }
    [data-testid="stMetricLabel"] { color: #738098; }
    [data-testid="stMetricValue"] { color: #202944; }
    h2, h3 { color: #202944 !important; }
    .section-note { color: #7b8599; font-size: 0.88rem; margin-top: -0.45rem; }
    div[data-testid="stDataFrame"] {
        border: 1px solid #e8ebf4;
        border-radius: 14px;
        overflow: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

rng = np.random.default_rng(42)
dates = pd.date_range("2025-01-01", periods=90, freq="D")

df = pd.DataFrame(
    {
        "date": dates,
        "sales": rng.integers(100, 250, size=len(dates)),
        "profit": rng.integers(40, 140, size=len(dates)),
        "visitors": rng.integers(300, 900, size=len(dates)),
        "channel": rng.choice(
            ["Online", "Retail", "Partner"],
            size=len(dates),
            p=[0.5, 0.3, 0.2],
        ),
    }
)
df["month"] = df["date"].dt.strftime("%b")
df["weekday"] = df["date"].dt.day_name()

st.sidebar.markdown("## Dashboard")
st.sidebar.caption("A colorful tour of Streamlit charts")
st.sidebar.markdown("---")
st.sidebar.subheader("Dashboard controls")
days_to_show = st.sidebar.slider("Days to include", min_value=7, max_value=90, value=30)
show_raw_data = st.sidebar.toggle("Show sample data table", value=True)
filtered_df = df.tail(days_to_show).copy()

st.markdown(
    """
    <div class="hero">
        <div class="eyebrow">Analytics overview · Sample workspace</div>
        <h1>Data, at a glance <span aria-hidden="true">✦</span></h1>
        <p>Explore a gallery of chart types. Adjust the date range in the sidebar
        and watch the metrics and visualizations respond.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.subheader("At a glance")
metric1, metric2, metric3, metric4 = st.columns(4)
metric1.metric("Total sales", f"${filtered_df['sales'].sum():,.0f}", f"Last {days_to_show} days")
metric2.metric("Average profit", f"${filtered_df['profit'].mean():,.0f}", "Per day")
metric3.metric("Total visitors", f"{filtered_df['visitors'].sum():,}", "In selected period")
metric4.metric("Avg. conversion", f"{filtered_df['sales'].sum() / filtered_df['visitors'].sum() * 100:.1f}%", "Sales / visitors")

plotly_layout = {
    "template": "plotly_white",
    "color_discrete_sequence": COLORS,
    "height": 330,
}

st.markdown("### Chart gallery")
st.markdown(
    '<p class="section-note">Common chart styles for comparing trends, distributions, and proportions.</p>',
    unsafe_allow_html=True,
)

left, right = st.columns(2)
with left:
    with st.container(border=True):
        st.subheader("Line chart · Daily trend")
        line_fig = px.line(
            filtered_df,
            x="date",
            y=["sales", "profit"],
            labels={"value": "Amount ($)", "date": "Date", "variable": "Metric"},
            **plotly_layout,
        )
        line_fig.update_traces(line={"width": 3})
        st.plotly_chart(line_fig, use_container_width=True)

    with st.container(border=True):
        st.subheader("Bar chart · Sales by channel")
        channel_sales = filtered_df.groupby("channel", as_index=False)["sales"].sum()
        bar_fig = px.bar(
            channel_sales,
            x="channel",
            y="sales",
            color="channel",
            labels={"channel": "Channel", "sales": "Sales ($)"},
            **plotly_layout,
        )
        bar_fig.update_layout(showlegend=False)
        st.plotly_chart(bar_fig, use_container_width=True)

    with st.container(border=True):
        st.subheader("Histogram · Sales distribution")
        histogram_fig = px.histogram(
            filtered_df,
            x="sales",
            nbins=12,
            labels={"sales": "Daily sales ($)", "count": "Number of days"},
            **plotly_layout,
        )
        histogram_fig.update_traces(marker_line_color="white", marker_line_width=1)
        st.plotly_chart(histogram_fig, use_container_width=True)

    with st.container(border=True):
        st.subheader("Pie chart · Sales by channel")
        pie_fig = px.pie(
            channel_sales,
            names="channel",
            values="sales",
            hole=0,
            **plotly_layout,
        )
        st.plotly_chart(pie_fig, use_container_width=True)

with right:
    with st.container(border=True):
        st.subheader("Area chart · Visitor activity")
        area_fig = px.area(
            filtered_df,
            x="date",
            y="visitors",
            labels={"visitors": "Visitors", "date": "Date"},
            **plotly_layout,
        )
        st.plotly_chart(area_fig, use_container_width=True)

    with st.container(border=True):
        st.subheader("Scatter plot · Sales vs. profit")
        scatter_fig = px.scatter(
            filtered_df,
            x="sales",
            y="profit",
            color="channel",
            size="visitors",
            hover_data=["date"],
            labels={"sales": "Sales ($)", "profit": "Profit ($)", "channel": "Channel"},
            **plotly_layout,
        )
        st.plotly_chart(scatter_fig, use_container_width=True)

    with st.container(border=True):
        st.subheader("Box plot · Daily sales by channel")
        box_fig = px.box(
            filtered_df,
            x="channel",
            y="sales",
            color="channel",
            labels={"channel": "Channel", "sales": "Daily sales ($)"},
            **plotly_layout,
        )
        box_fig.update_layout(showlegend=False)
        st.plotly_chart(box_fig, use_container_width=True)

    with st.container(border=True):
        st.subheader("Donut chart · Visitor share")
        channel_visitors = filtered_df.groupby("channel", as_index=False)["visitors"].sum()
        donut_fig = px.pie(
            channel_visitors,
            names="channel",
            values="visitors",
            hole=0.58,
            **plotly_layout,
        )
        st.plotly_chart(donut_fig, use_container_width=True)

with st.container(border=True):
    st.subheader("Correlation heatmap · How metrics move together")
    correlation_fig = px.imshow(
        filtered_df[["sales", "profit", "visitors"]].corr(),
        text_auto=".2f",
        color_continuous_scale=["#F45B8D", "#FFFFFF", "#5B6CFF"],
        zmin=-1,
        zmax=1,
        aspect="auto",
        height=300,
    )
    correlation_fig.update_layout(
        template="plotly_white",
        margin={"l": 16, "r": 16, "t": 20, "b": 16},
        coloraxis_colorbar_title="Correlation",
    )
    st.plotly_chart(correlation_fig, use_container_width=True)

if show_raw_data:
    with st.container(border=True):
        st.subheader("Sample data")
        st.markdown(
            '<p class="section-note">Records included in the selected time period.</p>',
            unsafe_allow_html=True,
        )
        st.dataframe(filtered_df, use_container_width=True, hide_index=True)

st.markdown(
    '<p class="section-note" style="text-align:center; padding-top:1.5rem;">Built with Streamlit and Plotly · Adjust the sidebar controls to explore interactive charts.</p>',
    unsafe_allow_html=True,
)
