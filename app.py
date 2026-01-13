import streamlit as st
import pandas as pd
import re
import urllib.parse

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

st.title("🔍 אפליקציית חיפוש והשוואת מחירים")

item = st.text_input("מה המוצר שאתה מחפש?")
price_input = st.text_input("מה המחיר המקורי?", value="0")
company = st.text_input("חברה מועדפת והנחה (למשל: KSP 15%)")
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
        discount_percent = 0
        
        if company:
            match = re.search(r'(\d+)%', company)
            if match:
                discount_percent = int(match.group(1))
                final_price = price * (1 - discount_percent / 100)
            company_name = re.sub(r'\s*\d+%.*', '', company).strip() or company.split()[0]
        
        st.subheader(f"תוצאות עבור: {item}")
        
        # חישוב מחירים משוערים
        amazon_price = price * 0.95  # 5% יותר זול בממוצע
        aliexpress_min = price * 0.60  # 40% הנחה
        aliexpress_max = price * 0.80  # 20% הנחה
        yad2_min = price * 0.50  # 50% הנחה
        yad2_max = price * 0.75  # 25% הנחה
        
        # יצירת קישורים
        item_encoded = urllib.parse.quote(item)
        
        data = {
            "חנות": ["🌍 אמזון", "🇨🇳 אלי אקספרס", f"⭐ {company_name}", "🤝 יד שנייה"],
            "מחיר משוער": [
                f"₪{amazon_price:,.0f}",
                f"₪{aliexpress_min:,.0f} - ₪{aliexpress_max:,.0f}",
                f"₪{final_price:,.0f}" + (f" (הנחה {discount_percent}%)" if discount_percent > 0 else ""),
                f"₪{yad2_min:,.0f} - ₪{yad2_max:,.0f}"
            ],
            "סטטוס": ["זמין", "זמין", "מומלץ", "לבדוק"]
        }
        
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # חיסכון
        if final_price < price:
            savings = price - final_price
            st.success(f"💰 חיסכון במחיר המועדף: ₪{savings:,.0f}")
        
        # הערות
        if notes.strip():
            st.info(f"📝 הערה: {notes}")
        
        # קישורים לחיפוש
        st.markdown("---")
        st.subheader("🔗 חפש באתרים:")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            amazon_url = f"https://www.amazon.com/s?k={item_encoded}"
            st.markdown(f"[🌍 חפש באמזון]({amazon_url})")
        
        with col2:
            ali_url = f"https://www.aliexpress.com/wholesale?SearchText={item_encoded}"
            st.markdown(f"[🇨🇳 חפש באלי אקספרס]({ali_url})")
        
        with col3:
            yad2_url = f"https://www.yad2.co.il/products/search?query={item_encoded}"
            st.markdown(f"[🤝 חפש ביד2]({yad2_url})")
        
        # קישורים נוספים
        col4, col5 = st.columns(2)
        
        with col4:
            zap_url = f"https://www.zap.co.il/search.aspx?keyword={item_encoded}"
            st.markdown(f"[💡 חפש בזאפ]({zap_url})")
        
        with col5:
            ksp_url = f"https://ksp.co.il/web/cat/573..2008?q={item_encoded}"
            st.markdown(f"[🏪 חפש ב-KSP]({ksp_url})")

st.markdown("---")
st.caption("אפליקציה לחיפוש והשוואת מחירים | נוצר ע\"י נחמיה")
