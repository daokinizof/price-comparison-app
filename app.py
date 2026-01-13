import streamlit as st
import pandas as pd
import re
import urllib.parse
import requests
from bs4 import BeautifulSoup

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
price_input = st.text_input("מה המחיר המקורי? (אופציונלי)", value="0")
company = st.text_input("חברה מועדפת והנחה (למשל: KSP 15%)")
notes = st.text_area("הערות (מדינה, יד שניה וכו')")

if st.button("בצע חיפוש"):
    if not item.strip():
        st.warning("נא להזין שם מוצר")
    else:
        try:
            price = float(price_input.replace(',', ''))
        except ValueError:
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
        
        # חיפוש אמיתי בזאפ
        with st.spinner('מחפש בזאפ...'):
            try:
                item_encoded = urllib.parse.quote(item)
                zap_url = f"https://www.zap.co.il/search.aspx?keyword={item_encoded}"
                
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                
                response = requests.get(zap_url, headers=headers, timeout=5)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # מחפש מחירים בזאפ
                    price_elements = soup.find_all(class_=re.compile('price|Price'))
                    
                    if price_elements and len(price_elements) > 0:
                        # מצא מחיר!
                        zap_price_text = price_elements[0].get_text()
                        zap_price_match = re.search(r'([\d,]+)', zap_price_text)
                        
                        if zap_price_match:
                            zap_price = float(zap_price_match.group(1).replace(',', ''))
                            st.success(f"✅ נמצא בזאפ! מחיר: ₪{zap_price:,.0f}")
                            
                            if price > 0:
                                data = {
                                    "מקור": ["המחיר שהזנת", "זאפ (מחיר אמיתי)", f"{company_name}"],
                                    "מחיר": [
                                        f"₪{price:,.0f}",
                                        f"₪{zap_price:,.0f}",
                                        f"₪{final_price:,.0f}" + (f" (הנחה {discount_percent}%)" if discount_percent > 0 else "")
                                    ],
                                    "סטטוס": ["התחלתי מכאן", "✅ מחיר אמיתי", "מומלץ"]
                                }
                            else:
                                data = {
                                    "מקור": ["זאפ (מחיר אמיתי)", f"{company_name}"],
                                    "מחיר": [
                                        f"₪{zap_price:,.0f}",
                                        f"₪{zap_price * 0.9:,.0f}" + (f" (הנחה {discount_percent}%)" if discount_percent > 0 else " (הערכה)")
                                    ],
                                    "סטטוס": ["✅ מחיר אמיתי", "הערכה"]
                                }
                        else:
                            raise Exception("לא נמצא מחיר")
                    else:
                        raise Exception("לא נמצאו תוצאות")
                else:
                    raise Exception(f"שגיאה: {response.status_code}")
                    
            except Exception as e:
                st.warning(f"⚠️ לא הצלחתי לחפש בזאפ ({str(e)}) - מציג מחירים משוערים")
                
                # אם החיפוש נכשל - מחירים משוערים
                if price > 0:
                    data = {
                        "מקור": ["המחיר שהזנת", "אמזון (הערכה)", f"{company_name}"],
                        "מחיר": [
                            f"₪{price:,.0f}",
                            f"₪{price * 0.95:,.0f}",
                            f"₪{final_price:,.0f}" + (f" (הנחה {discount_percent}%)" if discount_percent > 0 else "")
                        ],
                        "סטטוס": ["התחלתי מכאן", "הערכה", "מומלץ"]
                    }
                else:
                    st.error("נא להזין מחיר כדי לראות השוואה")
                    st.stop()
        
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # חיסכון
        if final_price < price and price > 0:
            savings = price - final_price
            st.success(f"💰 חיסכון אפשרי: ₪{savings:,.0f}")
        
        # הערות
        if notes.strip():
            st.info(f"📝 הערה: {notes}")
        
        # קישורים
        st.markdown("---")
        st.subheader("🔗 חפש באתרים:")
        
        col1, col2, col3 = st.columns(3)
        
        item_encoded = urllib.parse.quote(item)
        
        with col1:
            zap_url = f"https://www.zap.co.il/search.aspx?keyword={item_encoded}"
            st.markdown(f"[💡 זאפ]({zap_url})")
        
        with col2:
            ksp_url = f"https://ksp.co.il/web/cat/573..2008?q={item_encoded}"
            st.markdown(f"[🏪 KSP]({ksp_url})")
        
        with col3:
            yad2_url = f"https://www.yad2.co.il/products/search?query={item_encoded}"
            st.markdown(f"[🤝 יד2]({yad2_url})")

st.markdown("---")
st.caption("אפליקציה לחיפוש והשוואת מחירים | נוצר ע\"י נחמיה")
