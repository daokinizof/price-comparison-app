import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="חיפוש מוצרים", layout="centered")

st.markdown("""
<style>
    h1 {
        text-align: center;
        color: #1f77b4;
    }
    .stButton button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        font-size: 18px;
        padding: 15px;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🔍 אפליקציית חיפוש והשוואה")

item = st.text_input("מה המוצר שאתה מחפש?")
price_input = st.text_input("מה המחיר המקורי?", value="0")
company = st.text_input("חברה מועדפת והנחה (למשל: KSP 50%)")
notes = st.text_area("הערות (מדינה, יד שניה וכו')")

if st.button("בצע חיפוש"):
    if not item.strip():
        st.warning("נא להזין שם מוצר")
    else:
        try:
            price = float(price_input.replace(',', ''))
        except ValueError:
            st.error("המחיר חייב להיות מספר")
            price = 0
        
        final_price = price
        company_name = "חנות מועדפת"
        
        if company:
            match = re.search(r'(\d+)%', company)
            if match:
                percent = int(match.group(1))
                final_price = price * (1 - percent / 100)
            company_name = re.sub(r'\s*\d+%.*', '', company).strip() or company.split()[0]
        
        st.subheader(f"תוצאות עבור: {item}")
        
        data = {
            "חנות": ["אמזון", "אלי אקספרס", company_name, "יד שנייה"],
            "מחיר": [
                f"₪{price:,.2f}", 
                "זול יותר", 
                f"₪{final_price:,.2f} (אחרי הנחה)" if final_price != price else f"₪{price:,.2f}",
                "משתנה"
            ],
            "סטטוס": ["זמין", "זמין", "מומלץ עבורך", "צריך לבדוק"]
        }
        
        df = pd.DataFrame(data)
        st.table(df)
        
        if final_price < price:
            savings = price - final_price
            st.success(f"💰 חיסכון: ₪{savings:,.2f}")
        
        if notes.strip():
            st.info(f"📝 הערה: {notes}")

st.markdown("---")
st.caption("אפליקציה לחיפוש והשוואת מחירים")
