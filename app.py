import streamlit as st
import pandas as pd
import re
import urllib.parse
import plotly.graph_objects as go

st.set_page_config(
    page_title="חיפוש והשוואת מחירים", 
    layout="centered", 
    page_icon="🔍",
    initial_sidebar_state="expanded"
)

if 'search_history' not in st.session_state:
    st.session_state.search_history = []
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

def add_to_history(item_name, stores_data):
    if item_name:
        history_item = {
            'item': item_name,
            'stores': stores_data,
            'timestamp': pd.Timestamp.now().strftime('%d/%m/%Y %H:%M')
        }
        st.session_state.search_history.insert(0, history_item)
        st.session_state.search_history = st.session_state.search_history[:10]

if st.session_state.dark_mode:
    bg_color = "#1a1a1a"
    text_color = "#ffffff"
    card_bg = "#2d2d2d"
    button_bg = "#3d5a80"
    button_hover = "#2c4562"
else:
    bg_color = "#ffffff"
    text_color = "#000000"
    card_bg = "#f0f2f6"
    button_bg = "#1f77b4"
    button_hover = "#1557a0"

st.markdown(f"""
<style>
    .stApp {{
        background-color: {bg_color};
        color: {text_color};
    }}
    h1, h2, h3, h4, h5, h6, p, span, div {{
        color: {text_color} !important;
    }}
    h1 {{
        text-align: center;
        color: {button_bg} !important;
        margin-bottom: 0;
    }}
    .stButton button {{
        width: 100%;
        background-color: {button_bg};
        color: white;
        font-size: 18px;
        padding: 15px;
        border-radius: 10px;
        font-weight: bold;
    }}
    .stButton button:hover {{
        background-color: {button_hover};
    }}
    .store-link {{
        text-align: center;
        padding: 20px;
        border-radius: 10px;
        background-color: {card_bg};
        margin: 10px 0;
    }}
    .history-item {{
        background-color: {card_bg};
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("⚙️ הגדרות")
    
    dark_mode_toggle = st.toggle("🌙 מצב לילה", value=st.session_state.dark_mode)
    if dark_mode_toggle != st.session_state.dark_mode:
        st.session_state.dark_mode = dark_mode_toggle
        st.rerun()
    
    st.markdown("---")
    
    st.subheader("📜 חיפושים אחרונים")
    
    if len(st.session_state.search_history) > 0:
        for idx, hist in enumerate(st.session_state.search_history[:5]):
            with st.container():
                st.markdown(f"""
                <div class="history-item">
                    <b>{hist['item']}</b><br>
                    <small>{hist['timestamp']}</small>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"🔄 חזור לחיפוש", key=f"hist_{idx}"):
                    st.session_state.reload_search = hist
        
        if st.button("🗑️ נקה היסטוריה"):
            st.session_state.search_history = []
            st.rerun()
    else:
        st.info("אין חיפושים קודמים")
    
    st.markdown("---")
    st.caption("נוצר ע״י מאור איתן © 2026")

st.title("🔍 חיפוש והשוואת מחירים")
st.caption("מצא את המחיר הטוב ביותר בקלות!")

tab1, tab2, tab3 = st.tabs(["🔗 חיפוש מהיר", "📊 השוואת מחירים", "💳 מחשבון תשלומים"])

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
    
    st.markdown("#### 💰 הזן מחירים והנחות:")
    
    st.markdown("##### 💡 זאפ")
    col1, col2 = st.columns([2, 1])
    with col1:
        zap_price = st.number_input("מחיר", min_value=0, value=0, step=10, key="zap_price")
    with col2:
        zap_discount = st.number_input("הנחה %", min_value=0, max_value=100, value=0, step=5, key="zap_discount")
    
    st.markdown("---")
    
    st.markdown("##### 🏪 KSP")
    col1, col2 = st.columns([2, 1])
    with col1:
        ksp_price = st.number_input("מחיר", min_value=0, value=0, step=10, key="ksp_price")
    with col2:
        ksp_discount = st.number_input("הנחה %", min_value=0, max_value=100, value=0, step=5, key="ksp_discount")
    
    st.markdown("---")
    
    st.markdown("##### 🤝 יד שנייה")
    col1, col2 = st.columns([2, 1])
    with col1:
        yad2_price = st.number_input("מחיר", min_value=0, value=0, step=10, key="yad2_price")
    with col2:
        yad2_discount = st.number_input("הנחה %", min_value=0, max_value=100, value=0, step=5, key="yad2_discount")
    
    st.markdown("---")
    
    with st.expander("➕ הוסף חנות נוספת"):
        other_store = st.text_input("שם החנות", placeholder="לדוגמה: iDigital")
        col1, col2 = st.columns([2, 1])
        with col1:
            other_price = st.number_input("מחיר", min_value=0, value=0, step=10, key="other_price")
        with col2:
            other_discount = st.number_input("הנחה %", min_value=0, max_value=100, value=0, step=5, key="other_discount")
    
    if st.button("🔍 השווה וראה את התוצאה!"):
        if item_compare:
            prices_data = []
            
            if zap_price > 0:
                final_zap = zap_price * (1 - zap_discount / 100)
                prices_data.append({
                    "store": "💡 זאפ",
                    "price": zap_price,
                    "discount": zap_discount,
                    "final_price": final_zap
                })
            
            if ksp_price > 0:
                final_ksp = ksp_price * (1 - ksp_discount / 100)
                prices_data.append({
                    "store": "🏪 KSP",
                    "price": ksp_price,
                    "discount": ksp_discount,
                    "final_price": final_ksp
                })
            
            if yad2_price > 0:
                final_yad2 = yad2_price * (1 - yad2_discount / 100)
                prices_data.append({
                    "store": "🤝 יד שנייה",
                    "price": yad2_price,
                    "discount": yad2_discount,
                    "final_price": final_yad2
                })
            
            if other_price > 0 and other_store:
                final_other = other_price * (1 - other_discount / 100)
                prices_data.append({
                    "store": f"⭐ {other_store}",
                    "price": other_price,
                    "discount": other_discount,
                    "final_price": final_other
                })
            
            if len(prices_data) > 0:
                add_to_history(item_compare, prices_data)
                
                prices_data.sort(key=lambda x: x['final_price'])
                
                df_data = {
                    "חנות": [d['store'] for d in prices_data],
                    "מחיר מקורי": [f"₪{d['price']:,}" for d in prices_data],
                    "הנחה": [f"{d['discount']}%" if d['discount'] > 0 else "-" for d in prices_data],
                    "מחיר סופי": [f"₪{d['final_price']:,.0f}" for d in prices_data]
                }
                
                df = pd.DataFrame(df_data)
                st.dataframe(df, use_container_width=True, hide_index=True)
                
                st.markdown("### 📊 השוואה ויזואלית")
                
                fig = go.Figure()
                
                fig.add_trace(go.Bar(
                    name='מחיר מקורי',
                    x=[d['store'] for d in prices_data],
                    y=[d['price'] for d in prices_data],
                    marker_color='lightblue'
                ))
                
                fig.add_trace(go.Bar(
                    name='מחיר סופי',
                    x=[d['store'] for d in prices_data],
                    y=[d['final_price'] for d in prices_data],
                    marker_color='green'
                ))
                
                fig.update_layout(
                    barmode='group',
                    title='השוואת מחירים',
                    xaxis_title='חנות',
                    yaxis_title='מחיר (₪)',
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                best_deal = min(prices_data, key=lambda x: x['final_price'])
                st.success(f"### 🏆 **ההצעה הטובה ביותר:** {best_deal['store']} - ₪{best_deal['final_price']:,.0f}")
                
                if best_deal['discount'] > 0:
                    savings = best_deal['price'] - best_deal['final_price']
                    st.info(f"💰 **חיסכון בחנות זו:** ₪{savings:,.0f} (הנחה של {best_deal['discount']}%)")
                
                if len(prices_data) > 1:
                    worst_deal = max(prices_data, key=lambda x: x['final_price'])
                    total_savings = worst_deal['final_price'] - best_deal['final_price']
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("💰 הזול ביותר", f"₪{best_deal['final_price']:,.0f}")
                    
                    with col2:
                        st.metric("💸 היקר ביותר", f"₪{worst_deal['final_price']:,.0f}")
                    
                    with col3:
                        st.metric("📊 הפרש", f"₪{total_savings:,.0f}")
                
                st.markdown("### 💬 שתף את ההשוואה")
                
                whatsapp_text = f"🔍 השוואת מחירים: {item_compare}%0A%0A"
                for d in prices_data:
                    whatsapp_text += f"{d['store']}: ₪{d['final_price']:,.0f}%0A"
                whatsapp_text += f"%0A🏆 הכי זול: {best_deal['store']} - ₪{best_deal['final_price']:,.0f}"
                
                whatsapp_url = f"https://wa.me/?text={whatsapp_text}"
                
                st.markdown(f"""
                <a href="{whatsapp_url}" target="_blank">
                    <button style="padding: 10px 30px; font-size: 16px; background-color: #25D366; color: white; border: none; border-radius: 5px; cursor: pointer; width: 100%;">
                        💬 שתף ב-WhatsApp
                    </button>
                </a>
                """, unsafe_allow_html=True)
                
            else:
                st.warning("⚠️ נא להזין לפחות מחיר אחד")
        else:
            st.warning("⚠️ נא להזין שם מוצר")

with tab3:
    st.markdown("### 💳 מחשבון תשלומים")
    st.info("💡 חשב כמה תשלם בתשלומים עם/בלי ריבית")
    
    calc_price = st.number_input("💰 מחיר המוצר", min_value=0, value=3000, step=100)
    
    col1, col2 = st.columns(2)
    
    with col1:
        num_payments = st.selectbox("🔢 מספר תשלומים", [1, 3, 6, 10, 12, 24, 36])
    
    with col2:
        interest_rate = st.number_input("📈 ריבית חודשית (%)", min_value=0.0, max_value=10.0, value=0.0, step=0.1)
    
    if st.button("🧮 חשב תשלומים"):
        if calc_price > 0:
            if interest_rate == 0:
                monthly_payment = calc_price / num_payments
                total_payment = calc_price
                total_interest = 0
            else:
                monthly_rate = interest_rate / 100
                monthly_payment = calc_price * (monthly_rate * (1 + monthly_rate)**num_payments) / ((1 + monthly_rate)**num_payments - 1)
                total_payment = monthly_payment * num_payments
                total_interest = total_payment - calc_price
            
            st.success(f"### 💳 תשלום חודשי: ₪{monthly_payment:,.2f}")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("💰 מחיר מקורי", f"₪{calc_price:,}")
            
            with col2:
                st.metric("💸 סה״כ לתשלום", f"₪{total_payment:,.0f}")
            
            with col3:
                st.metric("📊 עלות ריבית", f"₪{total_interest:,.0f}")
            
            st.markdown("### 📊 פירוט תשלומים")
            
            payments_data = []
            for i in range(1, num_payments + 1):
                payments_data.append({
                    'תשלום': f"תשלום {i}",
                    'סכום': monthly_payment
                })
            
            df_payments = pd.DataFrame(payments_data)
            
            fig = go.Figure(data=[
                go.Bar(
                    x=df_payments['תשלום'],
                    y=df_payments['סכום'],
                    marker_color='lightgreen',
                    text=[f"₪{p:,.0f}" for p in df_payments['סכום']],
                    textposition='auto'
                )
            ])
            
            fig.update_layout(
                title=f'פריסת {num_payments} תשלומים',
                xaxis_title='מספר תשלום',
                yaxis_title='סכום (₪)',
                height=400,
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            if total_interest > 0:
                st.warning(f"⚠️ **שים לב:** תשלם ₪{total_interest:,.0f} נוספים בגלל ריבית!")
            else:
                st.info("✅ אין ריבית - אתה משלם רק את המחיר המקורי!")

st.markdown("---")
st.caption("🔍2026 © אפליקציית חיפוש והשוואת מחירים | נוצר ע״י מאור איתן")
