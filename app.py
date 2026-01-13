import streamlit as st
import pandas as pd
import re
import urllib.parse
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import io

st.set_page_config(
    page_title="חיפוש והשוואת מחירים", 
    layout="wide", 
    page_icon="🔍",
    initial_sidebar_state="expanded"
)

if 'search_history' not in st.session_state:
    st.session_state.search_history = []
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False
if 'language' not in st.session_state:
    st.session_state.language = 'he'
if 'color_theme' not in st.session_state:
    st.session_state.color_theme = 'blue'

def add_to_history(item_name, stores_data):
    if item_name:
        history_item = {
            'item': item_name,
            'stores': stores_data,
            'timestamp': pd.Timestamp.now().strftime('%d/%m/%Y %H:%M')
        }
        st.session_state.search_history.insert(0, history_item)
        st.session_state.search_history = st.session_state.search_history[:10]

TEXTS = {
    'he': {
        'title': '🔍 חיפוש והשוואת מחירים',
        'subtitle': 'מצא את המחיר הטוב ביותר בקלות!',
        'settings': '⚙️ הגדרות',
        'dark_mode': '🌙 מצב לילה',
        'language': '🌍 שפה',
        'color_theme': '🎨 ערכת צבעים',
        'history': '📜 חיפושים אחרונים',
        'no_history': 'אין חיפושים קודמים',
        'clear_history': '🗑️ נקה היסטוריה',
        'search_tab': '🔗 חיפוש מהיר',
        'compare_tab': '📊 השוואת מחירים',
        'payments_tab': '💳 מחשבון תשלומים',
        'specs_tab': '📋 השוואת מפרטים',
        'coupons_tab': '🎁 קופונים',
    },
    'en': {
        'title': '🔍 Price Comparison',
        'subtitle': 'Find the best price easily!',
        'settings': '⚙️ Settings',
        'dark_mode': '🌙 Dark Mode',
        'language': '🌍 Language',
        'color_theme': '🎨 Color Theme',
        'history': '📜 Recent Searches',
        'no_history': 'No recent searches',
        'clear_history': '🗑️ Clear History',
        'search_tab': '🔗 Quick Search',
        'compare_tab': '📊 Compare Prices',
        'payments_tab': '💳 Payment Calculator',
        'specs_tab': '📋 Compare Specs',
        'coupons_tab': '🎁 Coupons',
    }
}

def t(key):
    return TEXTS[st.session_state.language].get(key, key)

THEMES = {
    'blue': {'primary': '#1f77b4', 'secondary': '#1557a0', 'accent': '#FF6B35'},
    'green': {'primary': '#2ecc71', 'secondary': '#27ae60', 'accent': '#e74c3c'},
    'purple': {'primary': '#9b59b6', 'secondary': '#8e44ad', 'accent': '#f39c12'},
    'red': {'primary': '#e74c3c', 'secondary': '#c0392b', 'accent': '#3498db'},
}

theme = THEMES[st.session_state.color_theme]

if st.session_state.dark_mode:
    bg_color = "#1a1a1a"
    text_color = "#ffffff"
    card_bg = "#2d2d2d"
else:
    bg_color = "#ffffff"
    text_color = "#000000"
    card_bg = "#f0f2f6"

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
        color: {theme['primary']} !important;
    }}
    .stButton button {{
        width: 100%;
        background-color: {theme['primary']};
        color: white;
        font-size: 18px;
        padding: 15px;
        border-radius: 10px;
        font-weight: bold;
    }}
    .stButton button:hover {{
        background-color: {theme['secondary']};
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
    @media (max-width: 768px) {{
        .stButton button {{
            font-size: 14px;
            padding: 10px;
        }}
    }}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title(t('settings'))
    
    dark_mode_toggle = st.toggle(t('dark_mode'), value=st.session_state.dark_mode)
    if dark_mode_toggle != st.session_state.dark_mode:
        st.session_state.dark_mode = dark_mode_toggle
        st.rerun()
    
    lang = st.selectbox(t('language'), ['עברית', 'English'], index=0 if st.session_state.language == 'he' else 1)
    new_lang = 'he' if lang == 'עברית' else 'en'
    if new_lang != st.session_state.language:
        st.session_state.language = new_lang
        st.rerun()
    
    color = st.selectbox(t('color_theme'), ['כחול', 'ירוק', 'סגול', 'אדום'], 
                         index=['blue', 'green', 'purple', 'red'].index(st.session_state.color_theme))
    new_color = {'כחול': 'blue', 'ירוק': 'green', 'סגול': 'purple', 'אדום': 'red'}[color]
    if new_color != st.session_state.color_theme:
        st.session_state.color_theme = new_color
        st.rerun()
    
    st.markdown("---")
    st.subheader(t('history'))
    
    if len(st.session_state.search_history) > 0:
        for idx, hist in enumerate(st.session_state.search_history[:5]):
            with st.container():
                st.markdown(f"""
                <div class="history-item">
                    <b>{hist['item']}</b><br>
                    <small>{hist['timestamp']}</small>
                </div>
                """, unsafe_allow_html=True)
        
        if st.button(t('clear_history')):
            st.session_state.search_history = []
            st.rerun()
    else:
        st.info(t('no_history'))
    
    st.markdown("---")
    st.caption("נוצר ע״י נחמיה © 2025")

st.title(t('title'))
st.caption(t('subtitle'))

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    t('search_tab'), 
    t('compare_tab'), 
    t('payments_tab'),
    t('specs_tab'),
    t('coupons_tab')
])

STORES = {
    'זאפ': 'https://www.zap.co.il/search.aspx?keyword=',
    'KSP': 'https://ksp.co.il/web/search?q=',
    'יד2': 'https://www.yad2.co.il/products/search?query=',
    'iDigital': 'https://www.idigital.co.il/search?q=',
    'Bug': 'https://www.bug.co.il/search?q=',
    'Ivory': 'https://www.ivory.co.il/catalog.php?act=cat&keyword=',
}

with tab1:
    st.markdown("### 🔍 חפש מוצר בחנויות")
    st.info("💡 **טיפ:** לחץ על החנות, מצא את המחיר, וחזור להשוואה")
    
    item = st.text_input("מה אתה מחפש?", placeholder="לדוגמה: אייפון 15 Pro", key="search_item")
    
    if item:
        item_encoded = urllib.parse.quote(item)
        st.success(f"✅ מחפש: **{item}**")
        
        st.markdown("### 🏪 בחר חנות:")
        
        cols = st.columns(3)
        for idx, (store_name, store_url) in enumerate(STORES.items()):
            with cols[idx % 3]:
                full_url = store_url + item_encoded
                st.markdown(f"""
                <div class="store-link">
                    <h4>{store_name}</h4>
                    <a href="{full_url}" target="_blank">
                        <button style="padding: 8px 20px; font-size: 14px; background-color: {theme['primary']}; color: white; border: none; border-radius: 5px; cursor: pointer; width: 100%;">
                            חפש
                        </button>
                    </a>
                </div>
                """, unsafe_allow_html=True)

with tab2:
    st.markdown("### 📊 השווה את המחירים שמצאת")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        item_compare = st.text_input("שם המוצר:", placeholder="אייפון 15 Pro", key="compare_item")
    with col2:
        budget = st.number_input("💰 תקציב מקסימלי", min_value=0, value=0, step=100)
    
    notes = st.text_area("📝 הערות על המוצר", placeholder="למשל: צבע, נפח אחסון, וכו'")
    
    st.markdown("#### 💰 הזן מחירים והנחות:")
    
    prices_data = []
    
    for store_name in ['זאפ', 'KSP', 'iDigital', 'Bug', 'יד2', 'Ivory']:
        with st.expander(f"🏪 {store_name}"):
            col1, col2 = st.columns([2, 1])
            with col1:
                price = st.number_input(f"מחיר", min_value=0, value=0, step=10, key=f"{store_name}_price")
            with col2:
                discount = st.number_input(f"הנחה %", min_value=0, max_value=100, value=0, step=5, key=f"{store_name}_discount")
            
            if price > 0:
                final_price = price * (1 - discount / 100)
                prices_data.append({
                    "store": f"🏪 {store_name}",
                    "price": price,
                    "discount": discount,
                    "final_price": final_price
                })
    
    with st.expander("➕ חנות נוספת"):
        other_store = st.text_input("שם החנות")
        col1, col2 = st.columns([2, 1])
        with col1:
            other_price = st.number_input("מחיר", min_value=0, value=0, step=10, key="other_price2")
        with col2:
            other_discount = st.number_input("הנחה %", min_value=0, max_value=100, value=0, step=5, key="other_discount2")
        
        if other_price > 0 and other_store:
            final_other = other_price * (1 - other_discount / 100)
            prices_data.append({
                "store": f"⭐ {other_store}",
                "price": other_price,
                "discount": other_discount,
                "final_price": final_other
            })
    
    if st.button("🔍 השווה וראה את התוצאה!"):
        if item_compare and len(prices_data) > 0:
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
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 📊 גרף עמודות")
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
                fig.update_layout(barmode='group', height=350)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("### 🥧 גרף עוגה")
                fig2 = px.pie(
                    values=[d['final_price'] for d in prices_data],
                    names=[d['store'] for d in prices_data],
                    title='התפלגות מחירים'
                )
                fig2.update_layout(height=350)
                st.plotly_chart(fig2, use_container_width=True)
            
            best_deal = min(prices_data, key=lambda x: x['final_price'])
            st.success(f"### 🏆 **ההצעה הטובה ביותר:** {best_deal['store']} - ₪{best_deal['final_price']:,.0f}")
            
            if budget > 0:
                if best_deal['final_price'] <= budget:
                    diff = budget - best_deal['final_price']
                    st.success(f"✅ **שווה לקנות!** המחיר בתוך התקציב (נשאר לך ₪{diff:,.0f})")
                else:
                    diff = best_deal['final_price'] - budget
                    st.warning(f"⚠️ **חורג מהתקציב** ב-₪{diff:,.0f}")
            
            if notes:
                st.info(f"📝 **הערות:** {notes}")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                csv = df.to_csv(index=False, encoding='utf-8-sig')
                st.download_button(
                    "💾 הורד CSV",
                    csv,
                    f"comparison_{item_compare}.csv",
                    "text/csv"
                )
            
            with col2:
                whatsapp_text = f"🔍 {item_compare}%0A%0A"
                for d in prices_data:
                    whatsapp_text += f"{d['store']}: ₪{d['final_price']:,.0f}%0A"
                whatsapp_text += f"%0A🏆 הכי זול: {best_deal['store']}"
                st.markdown(f'<a href="https://wa.me/?text={whatsapp_text}" target="_blank"><button style="padding: 10px; background-color: #25D366; color: white; border: none; border-radius: 5px; width: 100%; cursor: pointer;">💬 שתף</button></a>', unsafe_allow_html=True)
            
            with col3:
                if len(prices_data) > 1:
                    st.metric("📊 הפרש", f"₪{max(d['final_price'] for d in prices_data) - best_deal['final_price']:,.0f}")
        
        elif not item_compare:
            st.warning("⚠️ נא להזין שם מוצר")
        else:
            st.warning("⚠️ נא להזין לפחות מחיר אחד")

with tab3:
    st.markdown("### 💳 מחשבון תשלומים")
    
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
            
            payments_list = [monthly_payment] * num_payments
            fig = go.Figure(data=[
                go.Bar(x=[f"#{i+1}" for i in range(num_payments)], y=payments_list, marker_color='lightgreen')
            ])
            fig.update_layout(title=f'פריסת {num_payments} תשלומים', height=350)
            st.plotly_chart(fig, use_container_width=True)
            
            if total_interest > 0:
                st.warning(f"⚠️ תשלם ₪{total_interest:,.0f} נוספים בריבית!")

with tab4:
    st.markdown("### 📋 השוואת מפרטים טכניים")
    st.info("💡 השווה בין 2-3 מוצרים דומים")
    
    num_products = st.slider("כמה מוצרים להשוות?", 2, 3, 2)
    
    products = []
    cols = st.columns(num_products)
    
    for i in range(num_products):
        with cols[i]:
            st.markdown(f"#### מוצר {i+1}")
            name = st.text_input(f"שם", key=f"spec_name_{i}")
            price = st.number_input(f"מחיר", min_value=0, value=0, key=f"spec_price_{i}")
            spec1 = st.text_input(f"מפרט 1", placeholder="זיכרון", key=f"spec1_{i}")
            spec2 = st.text_input(f"מפרט 2", placeholder="מעבד", key=f"spec2_{i}")
            spec3 = st.text_input(f"מפרט 3", placeholder="מצלמה", key=f"spec3_{i}")
            rating = st.slider(f"דירוג", 1, 5, 4, key=f"rating_{i}")
            
            products.append({
                'name': name,
                'price': price,
                'spec1': spec1,
                'spec2': spec2,
                'spec3': spec3,
                'rating': rating
            })
    
    if st.button("📊 השווה מפרטים"):
        if all(p['name'] for p in products):
            comparison_data = {
                'מאפיין': ['שם', 'מחיר', 'מפרט 1', 'מפרט 2', 'מפרט 3', 'דירוג'],
            }
            
            for i, p in enumerate(products):
                comparison_data[f'מוצר {i+1}'] = [
                    p['name'],
                    f"₪{p['price']:,}",
                    p['spec1'] or '-',
                    p['spec2'] or '-',
                    p['spec3'] or '-',
                    '⭐' * p['rating']
                ]
            
            df_comp = pd.DataFrame(comparison_data)
            st.dataframe(df_comp, use_container_width=True, hide_index=True)
            
            best_price_idx = min(range(len(products)), key=lambda i: products[i]['price'] if products[i]['price'] > 0 else float('inf'))
            best_rating_idx = max(range(len(products)), key=lambda i: products[i]['rating'])
            
            st.success(f"💰 **הזול ביותר:** {products[best_price_idx]['name']} - ₪{products[best_price_idx]['price']:,}")
            st.success(f"⭐ **הדירוג הגבוה ביותר:** {products[best_rating_idx]['name']} - {products[best_rating_idx]['rating']}/5")
        else:
            st.warning("⚠️ נא למלא שמות לכל המוצרים")

with tab5:
    st.markdown("### 🎁 אתרי קופונים והנחות")
    st.info("💡 חפש קופונים לפני הקנייה וחסוך עוד יותר!")
    
    coupon_sites = {
        'זאפ דילים': 'https://www.zap.co.il/deals/',
        'פורטל המבצעים': 'https://www.portal.co.il/',
        'בזק דילס': 'https://www.bezek.deals/',
        'Honey': 'https://www.joinhoney.com/',
        'הוט דילס': 'https://www.hotdeals.co.il/',
        'פייסבוק מבצעים': 'https://www.facebook.com/groups/mbzaim/',
    }
    
    cols = st.columns(2)
    for idx, (site_name, site_url) in enumerate(coupon_sites.items()):
        with cols[idx % 2]:
            st.markdown(f"""
            <div class="store-link">
                <h4>🎁 {site_name}</h4>
                <a href="{site_url}" target="_blank">
                    <button style="padding: 10px 20px; background-color: {theme['accent']}; color: white; border: none; border-radius: 5px; cursor: pointer; width: 100%;">
                        לחץ לקופונים
                    </button>
                </a>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 💡 טיפים לחיסכון")
    
    tips = [
        "✅ חפש קופונים לפני כל קנייה",
        "✅ השווה מחירים ב-3 חנויות לפחות",
        "✅ קנה בימי מבצעים (שישי שחור, סייבר מנדיי)",
        "✅ הירשם לניוזלטרים של החנויות",
        "✅ שתף עגלה ותחזור אחרי יום - לפעמים יש הנחה",
        "✅ השתמש בכרטיסי אשראי עם הטבות",
    ]
    
    for tip in tips:
        st.markdown(f"- {tip}")

st.markdown("---")
st.caption("🔍 אפליקציית חיפוש והשוואת מחירים מתקדמת | נוצר ע״י נחמיה © 2025")
