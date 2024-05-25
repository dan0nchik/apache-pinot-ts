import streamlit as st

# main page
def main():
    st.title("Software system for assessing the impact of news on stock prices") 

    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Choose a page", ["News", "Stocks"])

    if page == "News":
        news_page()
    elif page == "Stocks":
        stocks_page()

# new
def news_page():
    st.title("News")
    news_options = ["Option 1", "Option 2", "Option 3"]
    selected_news = st.selectbox("Select a news option", news_options)
    st.write(f"You selected: {selected_news}")

# stocks
def stocks_page():
    st.title("Stocks")
    stocks_options = ["AAPL", "ASTR", "GOOGL", "SBER", "TSLA", "VTBR"]
    selected_stock = st.selectbox("Select a stock option", stocks_options)
    
    if selected_stock == "AAPL":
        stock_a_page()
    elif selected_stock == "ASTR":
        stock_b_page()
    elif selected_stock == "GOOGL":
        stock_c_page()
    elif selected_stock == "SBER":
        stock_d_page()
    elif selected_stock == "TSLA":
        stock_e_page()
    elif selected_stock == "VTBR":
        stock_f_page()

def stock_a_page():
    st.header("AAPL")
    st.write("Graph")

    st.line_chart([1, 3, 2, 4, 5])

def stock_b_page():
    st.header("ASTR")
    st.write("Graph")

    st.line_chart([1, 3, 2, 4, 5])

def stock_c_page():
    st.header("GOOGL")
    st.write("Graph")

    st.line_chart([1, 3, 2, 4, 5])

def stock_d_page():
    st.header("SBER")
    st.write("Graph")

    st.line_chart([2, 3, 1, 5, 4])

def stock_e_page():
    st.header("TSLA")
    st.write("Graph")

    st.line_chart([1, 3, 2, 4, 5])    

def stock_f_page():
    st.header("VTBR")
    st.write("Graph")

    st.line_chart([5, 3, 2, 1, 4])

if __name__ == "__main__":
    main()
