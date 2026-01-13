import streamlit as st
import pandas as pd
import re
import urllib.parse

st.set_page_config(page_title="חיפוש והשוואת מחירים", layout="centered", page_icon="🔍")

st.markdown("""
<style>
    h1 {
        text-align: center;
        color: #1f77b4;
        margin-bottom: 0;
    }
    .stButton button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        font-size: 18px;
        padding: 15px;
        border-radius: 10px;
        font-weight: bold;
    }
    .stButton button:hover {
        background-color: #1557a0;
    }
    .store-link {
        text-align: center;
        padding: 20px;
        border-radius: 10px;
        background-color: #f0f2f6;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

st.title("🔍 חיפוש והשוואת מחירים")
st.caption("מצא את המחיר הטוב ביותר בקלות!")

tab1, tab2 = st.tabs(["🔗 חיפוש מהיר", "📊 השוואת מחירים"])

with tab1:
    st.markdown("### 🔍 חפש מוצר בחנויות")
    st.info("💡 **טיפ:** לחץ על החנות, מצא את המחיר, וחזור להשוואה בטאב 'השוואת מחירים'")
    
    item = st.text_input("מה אתה מחפש?", placeholder="לדוגמה: אייפון 15 Pro", key="search_item")
    
    if item:
        item_encoded = urllib.parse.quote(item)
        
        st.success(f"✅ מחפש: **{item}**")
        
        st.markdown("### 🏪 לחץ על חנות לחיפוש:")
        
        zap_url = f"https://www.zap.co.il/search.aspx?keyword={item_encoded}"
        st.markdown(f"""
        <div class="store-link">
            <h3>💡 זאפ</h3>
            <p>השוואת מחירים מכל החנויות בישראל</p>
            <a href="{zap_url}" target="_blank">
                <button style="padding: 10px 30px; font-size: 16px; background-color: #FF6B35; color: white; border: none; border-radius: 5px; cursor: pointer;">
                    🔍 חפש בזאפ
                </button>
            </a>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            ksp_url = f"https://ksp.co.il/web/search?q={item_encoded}"
            st.markdown(f"""
            <div class="store-link">
                <h4>🏪 KSP</h4>
                <a href="{ksp_url}" target="_blank">
                    <button style="padding: 8px 20px; font-size: 14px; background-color: #4CAF50; color: white; border: none; border-radius: 5px; cursor: pointer;">
                        חפש ב-KSP
                    </button>
                </a>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            yad2_url = f"https://www.yad2.co.il/products/search?query={item_encoded}"
            st.markdown(f"""
            <div class="store-link">
                <h4>🤝 יד שנייה</h4>
                <a href="{yad2_url}" target="_blank">
                    <button style="padding: 8px 20px; font-size: 14px; background-color: #FF9800; color: white; border: none; border-radius: 5px; cursor: pointer;">
                        חפש ביד2
                    </button>
                </a>
            </div>
            """, unsafe_allow_html=True)

with tab2:
    st.markdown("### 📊 השווה את המחירים שמצאת")
    st.info("💡 הזן את המחירים שמצאת בחנויות השונות ונראה איפה הכי כדאי!")
    
    item_compare = st.text_input("שם המוצר:", placeholder="לדוגמה: אייפון 15 Pro", key="compare_item")
    
    st.markdown("#### 💰 הזן מחירים:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        zap_price = st.number_input("💡 מחיר בזאפ", min_value=0, value=0, step=10, help="המחיר הזול ביותר שמצאת בזאפ")
    
    with col2:
        ksp_price = st.number_input("🏪 מחיר ב-KSP", min_value=0, value=0, step=10)
    
    with col3:
        yad2_price = st.number_input("🤝 מחיר ביד2", min_value=0, value=0, step=10)
    
    with st.expander("➕ הוסף חנות נוספת"):
        other_store = st.text_input("שם החנות", placeholder="לדוגמה: iDigital")
        other_price = st.number_input("מחיר", min_value=0, value=0, step=10, key="other")
    
    st.markdown("#### 🎁 יש לך קופון או הנחה?")
    discount_type = st.radio("", ["אין הנחה", "אחוז הנחה", "סכום קבוע"], horizontal=True)
    
    discount_value = 0
    if discount_type == "אחוז הנחה":
        discount_value = st.slider("כמה אחוז?", 0, 50, 10, 5)
    elif discount_type == "סכום קבוע":
        discount_value = st.number_input("כמה שקלים הנחה?", min_value=0, value=0, step=10)
    
    if st.button("🔍 השווה וראה את התוצאה!"):
        if item_compare:
            prices_data = []
            
            if zap_price > 0:
                prices_data.append({"store": "💡 זאפ", "price": zap_price})
            
            if ksp_price > 0:
                prices_data.append({"store": "🏪 KSP", "price": ksp_price})
            
            if yad2_price > 0:
                prices_data.append({"store": "🤝 יד שנייה", "price": yad2_price})
            
            if other_price > 0 and other_store:
                prices_data.append({"store": f"⭐ {other_store}", "price": other_price})
            
            if len(prices_data) > 0:
                prices_data.sort(key=lambda x: x['price'])
                
                for item_data in prices_data:
                    if discount_type == "אחוז הנחה":
                        item_data['final_price'] = item_data['price'] * (1 - discount_value / 100)
                    elif discount_type == "סכום קבוע":
                        item_data['final_price'] = max(0, item_data['price'] - discount_value)
                    else:
                        item_data['final_price'] = item_data['price']
                
                df_data = {
                    "חנות": [d['store'] for d in prices_data],
                    "מחיר": [f"₪{d['price']:,}" for d in prices_data],
                }
                
                if discount_type != "אין הנחה":
                    df_data["אחרי הנחה"] = [f"₪{d['final_price']:,.0f}" for d in prices_data]
                
                df = pd.DataFrame(df_data)
                st.dataframe(df, use_container_width=True, hide_index=True)
                
                best_deal = min(prices_data, key=lambda x: x['final_price'])
                st.success(f"### 🏆 **ההצעה הטובה ביותר:** {best_deal['store']} - ₪{best_deal['final_price']:,.0f}")
                
                if len(prices_data) > 1:
                    worst_deal = max(prices_data, key=lambda x: x['final_price'])
                    total_savings = worst_deal['final_price'] - best_deal['final_price']
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("💰 הזול ביותר", f"₪{best_deal['final_price']:,.0f}")
                    
                    with col2:
                        st.metric("💸 היקר ביותר", f"₪{worst_deal['final_price']:,.0f}")
                    
                    with col3:
                        st.metric("📊 חיסכון מקסימלי", f"₪{total_savings:,.0f}")
                
                if discount_type != "אין הנחה":
                    if discount_type == "אחוז הנחה":
                        actual_discount = best_deal['price'] - best_deal['final_price']
                        st.info(f"💡 **עם ההנחה שלך ({discount_value}%)** אתה חוסך ₪{actual_discount:,.0f} נוספים!")
                    else:
                        st.info(f"💡 **עם ההנחה שלך** אתה חוסך ₪{discount_value:,} נוספים!")
                
            else:
                st.warning("⚠️ נא להזין לפחות מחיר אחד")
        else:
            st.warning("⚠️ נא להזין שם מוצר")

st.markdown("---")
st.caption("🔍 אפליקציית חיפוש והשוואת מחירים | נוצר ע״י נחמיה © 2025")
