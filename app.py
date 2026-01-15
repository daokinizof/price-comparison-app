import streamlit as st
import pandas as pd
from datetime import datetime
import json

# =====================================
# הגדרות עמוד
# =====================================
st.set_page_config(
    page_title="חיפוש והשוואת מחירים | Price Comparison",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================
# פונקציות עזר
# =====================================

def load_legal_document(filename):
    """טוען מסמך משפטי מקובץ markdown"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return f"⚠️ המסמך {filename} לא נמצא. אנא וודא שהקובץ קיים בתיקייה."
    except Exception as e:
        return f"⚠️ שגיאה בטעינת המסמך: {str(e)}"

def show_legal_page(doc_type):
    """מציג דף משפטי לפי סוג"""
    docs = {
        "terms": ("terms_of_service.md", "📋 תנאי שימוש / Terms of Service"),
        "privacy": ("privacy_policy.md", "🔒 מדיניות פרטיות / Privacy Policy"),
        "disclosure": ("affiliate_disclosure_disclaimer.md", "📢 גילוי שותפות והצהרת אחריות / Affiliate Disclosure & Disclaimer")
    }
    
    if doc_type in docs:
        filename, title = docs[doc_type]
        
        # כותרת
        st.title(title)
        st.markdown("---")
        
        # כפתור חזרה
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if st.button("⬅️ חזרה לאפליקציה / Back to App", use_container_width=True):
                st.session_state.page = "main"
                st.rerun()
        
        st.markdown("---")
        
        # תוכן המסמך
        content = load_legal_document(filename)
        st.markdown(content, unsafe_allow_html=True)
        
        # כפתור חזרה נוסף בתחתית
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if st.button("⬅️ חזרה לאפליקציה / Back to App", key="back_bottom", use_container_width=True):
                st.session_state.page = "main"
                st.rerun()
    else:
        st.error("❌ מסמך לא נמצא / Document not found")

def add_legal_sidebar():
    """מוסיף קישורים למסמכים משפטיים בסיידבר"""
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ⚖️ מסמכים משפטיים / Legal")
    
    # כפתורים למסמכים
    if st.sidebar.button("📋 תנאי שימוש\nTerms of Service", use_container_width=True):
        st.session_state.page = "terms"
        st.rerun()
    
    if st.sidebar.button("🔒 מדיניות פרטיות\nPrivacy Policy", use_container_width=True):
        st.session_state.page = "privacy"
        st.rerun()
    
    if st.sidebar.button("📢 גילוי שותפות\nAffiliate Disclosure", use_container_width=True):
        st.session_state.page = "disclosure"
        st.rerun()
    
    # גילוי שותפות קצר (חובה!)
    st.sidebar.markdown("---")
    st.sidebar.info("""
    **💰 גילוי שותפות**
    
    אנו משתתפים בתוכניות שותפות ומרוויחים עמלה מרכישות דרך הקישורים שלנו, ללא עלות נוספת עבורך.
    
    **Affiliate Disclosure**
    
    We participate in affiliate programs and earn commissions from purchases through our links at no extra cost to you.
    """)
    
    # זכויות יוצרים
    st.sidebar.markdown("---")
    st.sidebar.caption("© 2026 Price Comparison App\nAll rights reserved")

def show_affiliate_banner():
    """מציג באנר גילוי שותפות בראש הדף"""
    st.warning("""
    ### ⚠️ גילוי חשוב / Important Disclosure
    
    **עברית:** הקישורים באפליקציה זו הם קישורי שותפות. אנו מרוויחים עמלה מרכישות דרך הקישורים. 
    המחירים זהים עבורך, אך העמלה עוזרת לנו לתחזק את האפליקציה בחינם.
    
    **English:** Links in this app are affiliate links. We earn commissions from purchases through our links.
    Prices are the same for you, but commissions help us maintain the app for free.
    
    [📋 תנאים / Terms](#) | [🔒 פרטיות / Privacy](#) | [📢 גילוי מלא / Full Disclosure](#)
    """)

# =====================================
# אתחול Session State
# =====================================
if 'page' not in st.session_state:
    st.session_state.page = "main"

if 'search_history' not in st.session_state:
    st.session_state.search_history = []

if 'language' not in st.session_state:
    st.session_state.language = "he"  # he/en

if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

# =====================================
# CSS מותאם אישית
# =====================================
st.markdown("""
<style>
    /* גופנים */
    @import url('https://fonts.googleapis.com/css2?family=Heebo:wght@300;400;500;700&family=Roboto:wght@300;400;500;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Heebo', 'Roboto', sans-serif;
    }
    
    /* כפתורים */
    .stButton button {
        font-size: 16px;
        font-weight: 500;
        padding: 10px 24px;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    /* טבלאות */
    .dataframe {
        font-size: 14px !important;
        border-radius: 8px !important;
    }
    
    /* כרטיסים */
    .stMetric {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #dee2e6;
    }
    
    /* הסתרת תפריט */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* באנרים */
    .stAlert {
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# =====================================
# פונקציה ראשית - דף האפליקציה
# =====================================
def main_app():
    """הדף הראשי של האפליקציה"""
    
    # הצגת באנר גילוי שותפות
    show_affiliate_banner()
    
    # כותרת ראשית
    st.title("🔍 אפליקציית חיפוש והשוואת מחירים")
    st.markdown("### Price Comparison Application")
    st.markdown("---")
    
    # טאבים
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🔎 חיפוש מהיר / Quick Search",
        "📊 השוואת מחירים / Price Compare",
        "💳 מחשבון תשלומים / Payment Calculator",
        "📋 השוואת מפרטים / Specs Compare",
        "🎫 קופונים / Coupons"
    ])
    
    # ==================
    # טאב 1: חיפוש מהיר
    # ==================
    with tab1:
        st.subheader("🔎 חיפוש מהיר")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            search_query = st.text_input(
                "מה אתה מחפש? / What are you looking for?",
                placeholder="לדוגמה: iPhone 15 Pro, Sony WH-1000XM5...",
                key="quick_search"
            )
        
        with col2:
            st.write("")  # ריווח
            st.write("")  # ריווח
            search_button = st.button("🔍 חפש / Search", use_container_width=True)
        
        if search_button and search_query:
            # שמירת חיפוש בהיסטוריה
            st.session_state.search_history.append({
                'query': search_query,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            
            st.success(f"✅ מחפש: {search_query}")
            
            # סימולציה של תוצאות
            st.markdown("---")
            st.subheader("📦 תוצאות / Results")
            
            # יצירת דוגמה לתוצאות
            stores = ["Amazon", "AliExpress", "eBay", "Best Buy", "Walmart"]
            results = []
            
            for i, store in enumerate(stores):
                base_price = 999 + (i * 50)
                results.append({
                    "חנות / Store": store,
                    "מחיר / Price": f"${base_price}",
                    "משלוח / Shipping": "חינם / Free" if i % 2 == 0 else f"${10 + i*2}",
                    "דירוג / Rating": f"{'⭐' * (5-i)} ({4.5 - i*0.2}/5)",
                    "זמן אספקה / Delivery": f"{3 + i*2}-{5 + i*2} ימים / days"
                })
            
            df = pd.DataFrame(results)
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            # כפתורי קישור (Affiliate Links)
            st.markdown("### 🛒 קישורים לרכישה / Purchase Links")
            cols = st.columns(len(stores))
            
            for idx, col in enumerate(cols):
                with col:
                    # קישור אמיתי לחנויות (כאן תשים את קישורי האפיליאט שלך)
                    if stores[idx] == "Amazon":
                        link = f"https://www.amazon.com/s?k={search_query.replace(' ', '+')}"
                    elif stores[idx] == "AliExpress":
                        link = f"https://www.aliexpress.com/wholesale?SearchText={search_query.replace(' ', '+')}"
                    elif stores[idx] == "eBay":
                        link = f"https://www.ebay.com/sch/i.html?_nkw={search_query.replace(' ', '+')}"
                    elif stores[idx] == "Best Buy":
                        link = f"https://www.bestbuy.com/site/searchpage.jsp?st={search_query.replace(' ', '+')}"
                    else:
                        link = f"https://www.walmart.com/search?q={search_query.replace(' ', '+')}"
                    
                    st.link_button(
                        f"🛒 {stores[idx]}",
                        link,
                        use_container_width=True
                    )
        
        # היסטוריית חיפושים
        if st.session_state.search_history:
            with st.expander("📜 היסטוריית חיפושים / Search History"):
                for item in reversed(st.session_state.search_history[-10:]):  # 10 אחרונים
                    st.text(f"🕐 {item['timestamp']} - {item['query']}")
    
    # ==================
    # טאב 2: השוואת מחירים
    # ==================
    with tab2:
        st.subheader("📊 השוואת מחירים מפורטת")
        
        col1, col2 = st.columns(2)
        
        with col1:
            product_name = st.text_input("שם המוצר / Product Name", key="compare_product")
        
        with col2:
            num_stores = st.slider("כמה חנויות להשוות? / How many stores?", 2, 10, 5)
        
        if st.button("📊 השווה מחירים / Compare Prices", use_container_width=True):
            if product_name:
                st.success(f"✅ משווה מחירים עבור: {product_name}")
                
                # יצירת נתונים להשוואה
                stores_list = ["Amazon", "AliExpress", "eBay", "Best Buy", "Walmart", 
                              "Newegg", "Target", "B&H Photo", "Adorama", "Costco"][:num_stores]
                
                comparison_data = []
                for i, store in enumerate(stores_list):
                    base = 999
                    price = base + (i * 45)
                    shipping = 0 if i % 2 == 0 else 10 + (i * 2)
                    total = price + shipping
                    
                    comparison_data.append({
                        "מיקום / Rank": i + 1,
                        "חנות / Store": store,
                        "מחיר בסיס / Base Price": f"${price}",
                        "משלוח / Shipping": f"${shipping}" if shipping > 0 else "חינם / Free",
                        "סה\"כ / Total": f"${total}",
                        "חיסכון / Savings": f"${total - (base + 0)}" if i > 0 else "-"
                    })
                
                df_compare = pd.DataFrame(comparison_data)
                
                # הדגשת העסקה הטובה ביותר
                st.success("🏆 העסקה הטובה ביותר / Best Deal: " + stores_list[0])
                
                st.dataframe(df_compare, use_container_width=True, hide_index=True)
                
                # גרף השוואה
                try:
                    import plotly.express as px
                    
                    prices_for_chart = [int(row['סה"כ / Total'].replace('$','')) 
                                       for row in comparison_data]
                    
                    fig = px.bar(
                        x=stores_list,
                        y=prices_for_chart,
                        labels={'x': 'חנות / Store', 'y': 'מחיר כולל / Total Price ($)'},
                        title='השוואת מחירים ויזואלית / Visual Price Comparison',
                        color=prices_for_chart,
                        color_continuous_scale='RdYlGn_r'
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                except:
                    st.info("💡 התקן plotly לגרפים אינטראקטיביים: pip install plotly")
    
    # ==================
    # טאב 3: מחשבון תשלומים
    # ==================
    with tab3:
        st.subheader("💳 מחשבון תשלומים")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            price = st.number_input("מחיר המוצר / Product Price ($)", min_value=0.0, value=999.0, step=10.0)
        
        with col2:
            months = st.slider("מספר תשלומים / Number of Payments", 1, 36, 12)
        
        with col3:
            interest = st.number_input("ריבית שנתית / Annual Interest (%)", min_value=0.0, value=5.0, step=0.5)
        
        if st.button("💰 חשב / Calculate", use_container_width=True):
            # חישוב תשלום חודשי
            monthly_interest = interest / 100 / 12
            
            if monthly_interest > 0:
                monthly_payment = price * (monthly_interest * (1 + monthly_interest)**months) / \
                                 ((1 + monthly_interest)**months - 1)
            else:
                monthly_payment = price / months
            
            total_paid = monthly_payment * months
            total_interest = total_paid - price
            
            # תצוגת תוצאות
            st.markdown("---")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("תשלום חודשי / Monthly Payment", f"${monthly_payment:.2f}")
            
            with col2:
                st.metric("סה\"כ לתשלום / Total Payment", f"${total_paid:.2f}")
            
            with col3:
                st.metric("סה\"כ ריבית / Total Interest", f"${total_interest:.2f}")
            
            with col4:
                st.metric("תוספת אחוזים / Percentage Added", f"{(total_interest/price)*100:.1f}%")
            
            # טבלת פירוט תשלומים
            st.markdown("---")
            st.subheader("📋 פירוט תשלומים / Payment Breakdown")
            
            payment_schedule = []
            remaining = price
            
            for i in range(1, months + 1):
                interest_payment = remaining * monthly_interest
                principal_payment = monthly_payment - interest_payment
                remaining -= principal_payment
                
                payment_schedule.append({
                    "תשלום / Payment #": i,
                    "תשלום חודשי / Monthly": f"${monthly_payment:.2f}",
                    "קרן / Principal": f"${principal_payment:.2f}",
                    "ריבית / Interest": f"${interest_payment:.2f}",
                    "יתרה / Balance": f"${max(0, remaining):.2f}"
                })
            
            df_payments = pd.DataFrame(payment_schedule)
            st.dataframe(df_payments, use_container_width=True, hide_index=True)
    
    # ==================
    # טאב 4: השוואת מפרטים
    # ==================
    with tab4:
        st.subheader("📋 השוואת מפרטים טכניים")
        st.info("💡 הכנס מפרטים של עד 3 מוצרים להשוואה")
        
        col1, col2, col3 = st.columns(3)
        
        products = []
        
        for idx, col in enumerate([col1, col2, col3]):
            with col:
                st.markdown(f"### מוצר {idx + 1} / Product {idx + 1}")
                
                product = {
                    "name": st.text_input(f"שם / Name", key=f"spec_name_{idx}"),
                    "price": st.number_input(f"מחיר / Price ($)", min_value=0.0, key=f"spec_price_{idx}"),
                    "brand": st.text_input(f"יצרן / Brand", key=f"spec_brand_{idx}"),
                    "model": st.text_input(f"דגם / Model", key=f"spec_model_{idx}"),
                    "warranty": st.selectbox(f"אחריות / Warranty", 
                                            ["1 year", "2 years", "3 years", "5 years"], 
                                            key=f"spec_warranty_{idx}")
                }
                
                products.append(product)
        
        if st.button("🔄 השווה / Compare", use_container_width=True):
            # בניית טבלת השוואה
            comparison = {
                "מאפיין / Feature": ["שם / Name", "מחיר / Price", "יצרן / Brand", "דגם / Model", "אחריות / Warranty"],
            }
            
            for idx, product in enumerate(products):
                comparison[f"מוצר {idx + 1} / Product {idx + 1}"] = [
                    product["name"] or "-",
                    f"${product['price']:.2f}" if product['price'] > 0 else "-",
                    product["brand"] or "-",
                    product["model"] or "-",
                    product["warranty"]
                ]
            
            df_specs = pd.DataFrame(comparison)
            st.dataframe(df_specs, use_container_width=True, hide_index=True)
            
            # המלצה
            valid_products = [p for p in products if p['name'] and p['price'] > 0]
            if valid_products:
                best = min(valid_products, key=lambda x: x['price'])
                st.success(f"🏆 המוצר הזול ביותר / Cheapest Product: {best['name']} - ${best['price']:.2f}")
    
    # ==================
    # טאב 5: קופונים
    # ==================
    with tab5:
        st.subheader("🎫 קופונים והנחות")
        
        # דוגמאות לקופונים
        coupons = [
            {
                "store": "Amazon",
                "code": "SAVE20",
                "discount": "20% הנחה / 20% Off",
                "expiry": "31/01/2026",
                "link": "https://www.amazon.com"
            },
            {
                "store": "AliExpress",
                "code": "NEW15",
                "discount": "15% הנחה למשתמשים חדשים / 15% Off for New Users",
                "expiry": "28/02/2026",
                "link": "https://www.aliexpress.com"
            },
            {
                "store": "eBay",
                "code": "TECH10",
                "discount": "$10 הנחה על מוצרי טכנולוגיה / $10 Off Tech Items",
                "expiry": "15/02/2026",
                "link": "https://www.ebay.com"
            }
        ]
        
        for coupon in coupons:
            with st.container():
                col1, col2, col3, col4 = st.columns([2, 3, 2, 2])
                
                with col1:
                    st.markdown(f"### {coupon['store']}")
                
                with col2:
                    st.code(coupon['code'])
                    st.caption(coupon['discount'])
                
                with col3:
                    st.text(f"⏰ עד / Until: {coupon['expiry']}")
                
                with col4:
                    st.link_button("🛒 השתמש / Use Now", coupon['link'], use_container_width=True)
                
                st.markdown("---")

# =====================================
# ניהול ניווט בין דפים
# =====================================
def main():
    """פונקציה ראשית לניהול הניווט"""
    
    # הוספת סיידבר משפטי
    add_legal_sidebar()
    
    # ניווט לפי page state
    if st.session_state.page == "main":
        main_app()
    
    elif st.session_state.page == "terms":
        show_legal_page("terms")
    
    elif st.session_state.page == "privacy":
        show_legal_page("privacy")
    
    elif st.session_state.page == "disclosure":
        show_legal_page("disclosure")
    
    else:
        st.error("❌ דף לא קיים / Page not found")
        if st.button("🏠 חזרה לדף הבית / Back to Home"):
            st.session_state.page = "main"
            st.rerun()

# =====================================
# הרצת האפליקציה
# =====================================
if __name__ == "__main__":
    main()
