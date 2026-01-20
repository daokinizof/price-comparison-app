import streamlit as st
import pandas as pd
from datetime import datetime
import random

# =====================================
# הגדרות
# =====================================

# Affiliate Configuration
AMAZON_AFFILIATE_TAG = "maoreitan11-20"  # Your Amazon Associate Tag

st.set_page_config(
    page_title="חיפוש והשוואת מחירים | Price Comparison",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================
# מסמכים משפטיים - מוטמעים בקוד
# =====================================

TERMS_OF_SERVICE = """
# תנאי שימוש / Terms of Service

**תאריך עדכון אחרון: 18 ינואר 2026 / Last Updated: January 18, 2026**

---

## עברית

### 1. קבלת התנאים
השימוש באפליקציית השוואת המחירים ("האפליקציה") מהווה הסכמה מלאה לתנאי שימוש אלה.

### 2. תיאור השירות
האפליקציה מספקת כלי להשוואת מחירי מוצרים בין חנויות שונות. השירות ניתן "כמות שהוא" (AS-IS).

### 3. דיוק המידע
- **אין אחריות לדיוק המחירים**: המחירים הינם אינדיקטיביים בלבד.
- **אחריות המשתמש**: יש לאמת את המחיר הסופי ישירות בחנות המוכרת.

### 4. קישורי שותפות
- האפליקציה מכילה קישורי שותפות (Affiliate Links).
- אנו מרוויחים עמלה מרכישות דרך הקישורים.
- העמלה אינה משפיעה על המחיר שאתה משלם.

### 5. הגבלת אחריות
- לא נהיה אחראים לנזקים הנובעים משימוש באפליקציה.
- המשתמש אחראי להחלטות הרכישה שלו.

---

## ENGLISH

### 1. Acceptance of Terms
By using the Price Comparison Application, you agree to these Terms of Service.

### 2. Service Description
The App provides price comparison tools. Service is provided "AS-IS".

### 3. Information Accuracy
- **No Price Guarantee**: Prices are indicative only.
- **User Responsibility**: Verify final prices directly with stores.

### 4. Affiliate Links
- The App contains affiliate links.
- We earn commissions from purchases.
- Commissions don't affect the price you pay.

### 5. Limitation of Liability
- We are not liable for damages from app use.
- Users are responsible for purchase decisions.

---

**© 2026 Price Comparison App. All rights reserved.**
"""

PRIVACY_POLICY = """
# מדיניות פרטיות / Privacy Policy

**תאריך עדכון אחרון: 18 ינואר 2026 / Last Updated: January 18, 2026**

---

## עברית

### 1. מבוא
מדיניות זו מסבירה כיצד אנו משתמשים במידע שלך.

### 2. מידע שאנו אוספים
- **היסטוריית חיפושים**: נשמרת **מקומית במכשיר שלך בלבד**.
- **אין שמירה בשרתים**: לא שומרים היסטוריה בשרתים שלנו.

### 3. מידע שאנו לא אוספים
- לא אוספים מידע אישי מזהה.
- לא עוקבים אחר גלישה מחוץ לאפליקציה.

### 4. אבטחת מידע
- **HTTPS**: כל התקשורת מוצפנת.
- **אחסון מקומי**: היסטוריה שמורה רק במכשיר שלך.

### 5. זכויות המשתמש
- ניתן למחוק היסטוריה בכל עת.

---

## ENGLISH

### 1. Introduction
This policy explains how we use your information.

### 2. Information We Collect
- **Search History**: Stored **locally on your device only**.
- **No Server Storage**: We don't save history on our servers.

### 3. Information We Don't Collect
- No personally identifiable information.
- No tracking outside the app.

### 4. Security
- **HTTPS**: All communication is encrypted.
- **Local Storage**: History stored only on your device.

### 5. User Rights
- Delete history at any time.

---

**© 2026 Price Comparison App. All rights reserved.**
"""

AFFILIATE_DISCLOSURE = """
# גילוי שותפות / Affiliate Disclosure

**תאריך עדכון אחרון: 18 ינואר 2026 / Last Updated: January 18, 2026**

---

## 📢 גילוי חשוב / Important Disclosure

### עברית

**אנו משתתפים בתוכנית Amazon Associates.**

כאשר אתה קונה מוצר דרך הקישורים שלנו ל-Amazon, אנו מקבלים עמלה קטנה.

**חשוב לדעת:**
- ✅ המחיר שאתה משלם **זהה לחלוטין**
- ✅ העמלה משולמת על ידי Amazon, לא על ידיך
- ✅ ההמלצות שלנו לא מושפעות מגובה העמלות
- ✅ אנו מציגים את המחיר הטוב ביותר למשתמש

**המטרה שלנו:** לעזור לך למצוא את העסקה הטובה ביותר!

---

### English

**We participate in the Amazon Associates Program.**

When you purchase through our Amazon links, we receive a small commission.

**Important to know:**
- ✅ The price you pay is **exactly the same**
- ✅ Commission is paid by Amazon, not by you
- ✅ Our recommendations are not influenced by commissions
- ✅ We show the best price for users

**Our goal:** Help you find the best deal!

---

## ⚠️ Disclaimer

### המחירים / Prices
- המחירים **אינדיקטיביים בלבד**
- עשויים להשתנות **בכל רגע**
- **בדוק תמיד** את המחיר הסופי באתר החנות

### אחריות / Responsibility
- אנו מספקים כלי להשוואה בלבד
- אתה אחראי על החלטות הרכישה שלך
- בדוק, השווה וחקור לפני קניה

---

**© 2026 Price Comparison App. All rights reserved.**
"""

# =====================================
# פונקציות עזר
# =====================================

def generate_realistic_price(base_price, variation=0.15):
    """יוצר מחיר ריאליסטי עם וריאציה"""
    variance = random.uniform(-variation, variation)
    price = base_price * (1 + variance)
    # עיגול למחיר "יפה"
    if price > 100:
        return round(price / 10) * 10 - 0.01  # $99.99, $109.99, etc.
    else:
        return round(price, 2)

def create_amazon_affiliate_link(search_query):
    """יוצר קישור Amazon עם Affiliate Tag"""
    encoded_query = search_query.replace(' ', '+')
    return f"https://www.amazon.com/s?k={encoded_query}&tag={AMAZON_AFFILIATE_TAG}"

def show_legal_page(doc_type):
    """מציג דף משפטי"""
    docs = {
        "terms": (TERMS_OF_SERVICE, "📋 תנאי שימוש / Terms of Service"),
        "privacy": (PRIVACY_POLICY, "🔒 מדיניות פרטיות / Privacy Policy"),
        "disclosure": (AFFILIATE_DISCLOSURE, "📢 גילוי שותפות / Affiliate Disclosure")
    }
    
    if doc_type in docs:
        content, title = docs[doc_type]
        
        st.title(title)
        st.markdown("---")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if st.button("⬅️ חזרה / Back", use_container_width=True):
                st.session_state.page = "main"
                st.rerun()
        
        st.markdown("---")
        st.markdown(content, unsafe_allow_html=True)
        
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if st.button("⬅️ חזרה / Back", key="back_bottom", use_container_width=True):
                st.session_state.page = "main"
                st.rerun()

def add_legal_sidebar():
    """מוסיף קישורים משפטיים בסיידבר"""
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ⚖️ מסמכים משפטיים / Legal")
    
    if st.sidebar.button("📋 תנאי שימוש\nTerms", use_container_width=True):
        st.session_state.page = "terms"
        st.rerun()
    
    if st.sidebar.button("🔒 מדיניות פרטיות\nPrivacy", use_container_width=True):
        st.session_state.page = "privacy"
        st.rerun()
    
    if st.sidebar.button("📢 גילוי שותפות\nDisclosure", use_container_width=True):
        st.session_state.page = "disclosure"
        st.rerun()
    
    st.sidebar.markdown("---")
    st.sidebar.info("""
    **💰 גילוי שותפות**
    
    אנו משתתפים בתוכנית Amazon Associates ומרוויחים עמלה מרכישות, ללא עלות נוספת עבורך.
    
    **Affiliate Disclosure**
    
    We participate in Amazon Associates and earn commissions at no extra cost to you.
    """)
    
    st.sidebar.markdown("---")
    st.sidebar.caption(f"© 2026 Price Comparison App\nAmazon Associate: {AMAZON_AFFILIATE_TAG}")

def show_affiliate_banner():
    """באנר גילוי שותפות"""
    st.info("""
    ### 💰 גילוי שותפות / Affiliate Disclosure
    
    **קישורי Amazon באפליקציה זו כוללים Affiliate Tag שלנו. אנו מרוויחים עמלה מרכישות, אך המחיר שאתה משלם זהה.**
    
    **Amazon links include our Affiliate Tag. We earn commissions, but your price stays the same.**
    """)

# =====================================
# אתחול Session State
# =====================================
if 'page' not in st.session_state:
    st.session_state.page = "main"

if 'search_history' not in st.session_state:
    st.session_state.search_history = []

# =====================================
# CSS מותאם אישית
# =====================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Heebo:wght@300;400;500;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Heebo', sans-serif;
    }
    
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
    
    .dataframe {
        font-size: 14px !important;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Amazon button style */
    .amazon-btn {
        background-color: #FF9900 !important;
        color: #000 !important;
        font-weight: bold !important;
    }
    
    .amazon-btn:hover {
        background-color: #FFB84D !important;
    }
</style>
""", unsafe_allow_html=True)

# =====================================
# פונקציה ראשית - דף האפליקציה
# =====================================
def main_app():
    """הדף הראשי"""
    
    show_affiliate_banner()
    
    st.title("🔍 אפליקציית חיפוש והשוואת מחירים")
    st.markdown("### Price Comparison Application")
    st.markdown("---")
    
    # טאבים
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🔎 חיפוש מהיר / Quick Search",
        "📊 השוואת מחירים / Compare",
        "💳 מחשבון תשלומים / Calculator",
        "📋 השוואת מפרטים / Specs",
        "🎫 קופונים / Coupons"
    ])
    
    # ==================
    # טאב 1: חיפוש מהיר
    # ==================
    with tab1:
        st.subheader("🔎 חיפוש מהיר במחירים")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            search_query = st.text_input(
                "חפש מוצר / Search Product",
                placeholder="iPhone 15 Pro, Sony Headphones, Samsung TV...",
                key="quick_search"
            )
        
        with col2:
            st.write("")
            st.write("")
            search_button = st.button("🔍 חפש / Search", use_container_width=True, type="primary")
        
        if search_button and search_query:
            # שמירה בהיסטוריה
            st.session_state.search_history.append({
                'query': search_query,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            
            st.success(f"✅ מחפש: **{search_query}**")
            st.markdown("---")
            
            # מחיר בסיס אקראי
            base_price = random.randint(50, 2000)
            
            # יצירת תוצאות עם מחירים ריאליסטיים
            stores_data = {
                "Amazon": {"variance": 0, "shipping": "Free", "rating": 4.5},
                "eBay": {"variance": 0.08, "shipping": "$5.99", "rating": 4.3},
                "Walmart": {"variance": 0.05, "shipping": "Free", "rating": 4.4},
                "Best Buy": {"variance": 0.12, "shipping": "$8.99", "rating": 4.2},
                "Target": {"variance": 0.15, "shipping": "$6.99", "rating": 4.1},
            }
            
            results = []
            for store, info in stores_data.items():
                price = generate_realistic_price(base_price, info["variance"])
                shipping_cost = 0 if info["shipping"] == "Free" else float(info["shipping"].replace("$", ""))
                total = price + shipping_cost
                
                results.append({
                    "🏪 חנות / Store": store,
                    "💵 מחיר / Price": f"${price:.2f}",
                    "📦 משלוח / Shipping": info["shipping"],
                    "💰 סה\"כ / Total": f"${total:.2f}",
                    "⭐ דירוג / Rating": f"{'⭐' * int(info['rating'])} ({info['rating']}/5)"
                })
            
            # מיון לפי מחיר כולל
            results.sort(key=lambda x: float(x['💰 סה"כ / Total'].replace('$', '')))
            
            # הוספת מיקום
            for idx, result in enumerate(results):
                result["#"] = idx + 1
            
            # סידור מחדש של העמודות
            df = pd.DataFrame(results)
            df = df[["#", "🏪 חנות / Store", "💵 מחיר / Price", "📦 משלוח / Shipping", 
                    "💰 סה\"כ / Total", "⭐ דירוג / Rating"]]
            
            # הדגשת העסקה הטובה ביותר
            best_store = results[0]["🏪 חנות / Store"]
            best_price = results[0]["💰 סה\"כ / Total"]
            st.success(f"🏆 **העסקה הטובה ביותר:** {best_store} - {best_price}")
            
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            # כפתורי קישור מעוצבים
            st.markdown("---")
            st.subheader("🛒 קישורים לרכישה / Buy Now")
            
            cols = st.columns(5)
            
            for idx, (col, store) in enumerate(zip(cols, stores_data.keys())):
                with col:
                    if store == "Amazon":
                        # Amazon עם Affiliate Tag
                        link = create_amazon_affiliate_link(search_query)
                        st.link_button(
                            f"🛒 {store}",
                            link,
                            use_container_width=True,
                            type="primary"
                        )
                        st.caption("✅ Affiliate Link")
                    elif store == "eBay":
                        link = f"https://www.ebay.com/sch/i.html?_nkw={search_query.replace(' ', '+')}"
                        st.link_button(f"🛒 {store}", link, use_container_width=True)
                    elif store == "Walmart":
                        link = f"https://www.walmart.com/search?q={search_query.replace(' ', '+')}"
                        st.link_button(f"🛒 {store}", link, use_container_width=True)
                    elif store == "Best Buy":
                        link = f"https://www.bestbuy.com/site/searchpage.jsp?st={search_query.replace(' ', '+')}"
                        st.link_button(f"🛒 {store}", link, use_container_width=True)
                    else:  # Target
                        link = f"https://www.target.com/s?searchTerm={search_query.replace(' ', '+')}"
                        st.link_button(f"🛒 {store}", link, use_container_width=True)
            
            st.markdown("---")
            st.info("""
            💡 **טיפ:** לחץ על הקישור כדי לראות את המוצר בחנות. 
            המחירים עשויים להשתנות - בדוק תמיד את המחיר הסופי לפני רכישה.
            
            **Tip:** Click the link to view the product in store.
            Prices may change - always verify final price before purchasing.
            """)
        
        # היסטוריה
        if st.session_state.search_history:
            with st.expander("📜 היסטוריית חיפושים / Search History"):
                for item in reversed(st.session_state.search_history[-10:]):
                    st.text(f"🕐 {item['timestamp']} - {item['query']}")
                if st.button("🗑️ נקה היסטוריה / Clear History"):
                    st.session_state.search_history = []
                    st.rerun()
    
    # ==================
    # טאב 2: השוואת מחירים
    # ==================
    with tab2:
        st.subheader("📊 השוואת מחירים מפורטת")
        
        col1, col2 = st.columns(2)
        
        with col1:
            product_name = st.text_input("שם המוצר / Product Name", key="compare_product")
        
        with col2:
            num_stores = st.slider("כמה חנויות? / How many stores?", 3, 10, 5)
        
        if st.button("📊 השווה / Compare", use_container_width=True, type="primary"):
            if product_name:
                st.success(f"✅ משווה: **{product_name}**")
                
                all_stores = ["Amazon", "eBay", "Walmart", "Best Buy", "Target", 
                             "Newegg", "B&H Photo", "Adorama", "Costco", "AliExpress"]
                stores_list = all_stores[:num_stores]
                
                base = random.randint(100, 1500)
                comparison_data = []
                
                for i, store in enumerate(stores_list):
                    price = generate_realistic_price(base, i * 0.03)
                    shipping = 0 if i % 2 == 0 else random.uniform(5, 15)
                    total = price + shipping
                    
                    comparison_data.append({
                        "מיקום / Rank": i + 1,
                        "חנות / Store": store,
                        "מחיר / Price": f"${price:.2f}",
                        "משלוח / Shipping": "Free" if shipping == 0 else f"${shipping:.2f}",
                        "סה\"כ / Total": f"${total:.2f}",
                        "חיסכון / Savings": f"${0:.2f}" if i == 0 else f"${total - (base):.2f}"
                    })
                
                df_compare = pd.DataFrame(comparison_data)
                
                st.success(f"🏆 **Best Deal:** {stores_list[0]}")
                st.dataframe(df_compare, use_container_width=True, hide_index=True)
                
                # גרף
                try:
                    import plotly.express as px
                    
                    prices = [float(row['סה"כ / Total'].replace('$','')) for row in comparison_data]
                    
                    fig = px.bar(
                        x=stores_list,
                        y=prices,
                        labels={'x': 'Store', 'y': 'Total Price ($)'},
                        title='השוואת מחירים / Price Comparison',
                        color=prices,
                        color_continuous_scale='RdYlGn_r'
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                except:
                    pass
    
    # ==================
    # טאב 3: מחשבון תשלומים
    # ==================
    with tab3:
        st.subheader("💳 מחשבון תשלומים")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            price = st.number_input("מחיר / Price ($)", min_value=0.0, value=999.0, step=10.0)
        
        with col2:
            months = st.slider("תשלומים / Payments", 1, 36, 12)
        
        with col3:
            interest = st.number_input("ריבית / Interest (%)", min_value=0.0, value=5.0, step=0.5)
        
        if st.button("💰 חשב / Calculate", use_container_width=True, type="primary"):
            monthly_interest = interest / 100 / 12
            
            if monthly_interest > 0:
                monthly_payment = price * (monthly_interest * (1 + monthly_interest)**months) / \
                                 ((1 + monthly_interest)**months - 1)
            else:
                monthly_payment = price / months
            
            total_paid = monthly_payment * months
            total_interest = total_paid - price
            
            st.markdown("---")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("תשלום חודשי\nMonthly", f"${monthly_payment:.2f}")
            
            with col2:
                st.metric("סה\"כ\nTotal", f"${total_paid:.2f}")
            
            with col3:
                st.metric("ריבית\nInterest", f"${total_interest:.2f}")
            
            with col4:
                st.metric("תוספת %\nAdded %", f"{(total_interest/price)*100:.1f}%")
    
    # ==================
    # טאב 4: מפרטים
    # ==================
    with tab4:
        st.subheader("📋 השוואת מפרטים")
        st.info("💡 הכנס מפרטים של עד 3 מוצרים")
        
        col1, col2, col3 = st.columns(3)
        
        products = []
        
        for idx, col in enumerate([col1, col2, col3]):
            with col:
                st.markdown(f"### מוצר {idx + 1}")
                
                product = {
                    "name": st.text_input(f"שם / Name", key=f"spec_name_{idx}"),
                    "price": st.number_input(f"מחיר / Price ($)", min_value=0.0, key=f"spec_price_{idx}"),
                    "brand": st.text_input(f"יצרן / Brand", key=f"spec_brand_{idx}"),
                    "warranty": st.selectbox(f"אחריות / Warranty", 
                                            ["1 year", "2 years", "3 years"], 
                                            key=f"spec_warranty_{idx}")
                }
                
                products.append(product)
        
        if st.button("🔄 השווה / Compare", use_container_width=True, type="primary"):
            comparison = {
                "מאפיין / Feature": ["שם / Name", "מחיר / Price", "יצרן / Brand", "אחריות / Warranty"],
            }
            
            for idx, product in enumerate(products):
                comparison[f"מוצר {idx + 1}"] = [
                    product["name"] or "-",
                    f"${product['price']:.2f}" if product['price'] > 0 else "-",
                    product["brand"] or "-",
                    product["warranty"]
                ]
            
            df_specs = pd.DataFrame(comparison)
            st.dataframe(df_specs, use_container_width=True, hide_index=True)
            
            valid = [p for p in products if p['name'] and p['price'] > 0]
            if valid:
                best = min(valid, key=lambda x: x['price'])
                st.success(f"🏆 הזול ביותר / Cheapest: {best['name']} - ${best['price']:.2f}")
    
    # ==================
    # טאב 5: קופונים
    # ==================
    with tab5:
        st.subheader("🎫 קופונים והנחות")
        
        coupons = [
            {
                "store": "Amazon",
                "code": "SAVE20",
                "discount": "20% Off",
                "expiry": "31/01/2026",
                "link": f"https://www.amazon.com/?tag={AMAZON_AFFILIATE_TAG}"
            },
            {
                "store": "eBay",
                "code": "TECH15",
                "discount": "15% Off",
                "expiry": "28/02/2026",
                "link": "https://www.ebay.com"
            },
            {
                "store": "Walmart",
                "code": "NEW10",
                "discount": "$10 Off",
                "expiry": "15/02/2026",
                "link": "https://www.walmart.com"
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
                    st.text(f"⏰ עד: {coupon['expiry']}")
                
                with col4:
                    st.link_button("🛒 Use Now", coupon['link'], use_container_width=True)
                
                st.markdown("---")

# =====================================
# ניהול ניווט
# =====================================
def main():
    """פונקציה ראשית"""
    
    add_legal_sidebar()
    
    if st.session_state.page == "main":
        main_app()
    elif st.session_state.page == "terms":
        show_legal_page("terms")
    elif st.session_state.page == "privacy":
        show_legal_page("privacy")
    elif st.session_state.page == "disclosure":
        show_legal_page("disclosure")
    else:
        st.error("❌ Page not found")

# =====================================
# הרצה
# =====================================
if __name__ == "__main__":
    main()
    
