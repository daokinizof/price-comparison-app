import streamlit as st
import pandas as pd
from datetime import datetime

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
# מסמכים משפטיים - מוטמעים בקוד
# =====================================

TERMS_OF_SERVICE = """
# תנאי שימוש / Terms of Service

**תאריך עדכון אחרון: 15 ינואר 2026 / Last Updated: January 15, 2026**

---

## עברית

### 1. קבלת התנאים
השימוש באפליקציית השוואת המחירים ("האפליקציה") מהווה הסכמה מלאה לתנאי שימוש אלה. אם אינך מסכים לתנאים אלה, אנא הימנע משימוש באפליקציה.

### 2. תיאור השירות
האפליקציה מספקת כלי להשוואת מחירי מוצרים בין חנויות שונות. השירות ניתן "כמות שהוא" (AS-IS) וללא כל אחריות או התחייבות לדיוק, זמינות או התאמה למטרה מסוימת.

### 3. דיוק המידע
- **אין אחריות לדיוק המחירים**: המחירים המוצגים באפליקציה הינם אינדיקטיביים בלבד ועשויים להשתנות בכל עת ללא הודעה מוקדמת.
- **עדכון מחירים**: המחירים מתעדכנים מעת לעת, אך אין ערבות שהם משקפים את המחירים הנוכחיים בחנויות.
- **זמינות מוצרים**: אין ערבות לזמינות המוצרים המוצגים באפליקציה.
- **אחריות המשתמש**: על המשתמש לאמת את המחיר הסופי, זמינות המוצר ותנאי הרכישה ישירות בחנות המוכרת.

### 4. קישורים לאתרי צד שלישי
- האפליקציה מכילה קישורי שותפות (Affiliate Links) לחנויות ואתרים חיצוניים.
- איננו אחראים לתוכן, למדיניות הפרטיות או לפעולות של אתרים אלה.
- השימוש באתרים חיצוניים כפוף לתנאי השימוש שלהם.

### 5. הכנסות משותפויות (Affiliate Revenue)
- **גילוי מלא**: האפליקציה משתתפת בתוכניות שותפות של Amazon Associates, AliExpress ואחרים.
- **עמלות**: אנו מרוויחים עמלה כאשר משתמש רוכש מוצר דרך הקישורים באפליקציה.
- **ללא עלות נוספת**: העמלה אינה משפיעה על המחיר שהמשתמש משלם.
- **עצמאות**: המלצותינו אינן מושפעות מגובה העמלות.

### 6. קניין רוחני
- כל התכנים, העיצוב והקוד באפליקציה מוגנים בזכויות יוצרים.
- אין להעתיק, לשכפל או להפיץ את האפליקציה ללא אישור בכתב.
- שמות המותגים והלוגואים של החנויות הינם קניינם של בעליהם המקוריים.

### 7. הגבלת אחריות
- **נזקים עקיפים**: לא נהיה אחראים לכל נזק ישיר, עקיף, מקרי או תוצאתי הנובע משימוש או אי-שימוש באפליקציה.
- **החלטות רכישה**: המשתמש נושא באחריות מלאה להחלטות הרכישה שלו.
- **תקלות טכניות**: לא נישא באחריות לתקלות, הפסקות שירות או אובדן מידע.

### 8. פרטיות והגנת מידע
- איסוף ושימוש במידע מפורטים במדיניות הפרטיות שלנו.
- היסטוריית חיפושים נשמרת באופן מקומי במכשיר המשתמש בלבד.

### 9. שינויים בתנאי השימוש
- אנו שומרים לעצמנו את הזכות לשנות תנאים אלה בכל עת.
- השימוש המתמשך באפליקציה לאחר שינוי מהווה הסכמה לתנאים המעודכנים.

### 10. דין וסמכות שיפוט
- תנאים אלה כפופים לדיני מדינת ישראל.
- הסמכות הייחודית לדון בכל סכסוך תהיה לבתי המשפט המוסמכים בישראל.

---

## ENGLISH

### 1. Acceptance of Terms
By using the Price Comparison Application ("the App"), you agree to be bound by these Terms of Service. If you do not agree to these terms, please do not use the App.

### 2. Description of Service
The App provides a tool for comparing product prices across different stores. The service is provided "AS-IS" without any warranty or guarantee of accuracy, availability, or fitness for a particular purpose.

### 3. Information Accuracy
- **No Price Guarantee**: Prices displayed in the App are indicative only and may change at any time without prior notice.
- **Price Updates**: Prices are updated periodically, but there is no guarantee they reflect current store prices.
- **Product Availability**: There is no guarantee of product availability shown in the App.
- **User Responsibility**: Users must verify final prices, product availability, and purchase terms directly with the selling store.

### 4. Third-Party Links
- The App contains affiliate links to external stores and websites.
- We are not responsible for the content, privacy policies, or actions of these sites.
- Use of external websites is subject to their terms of service.

### 5. Affiliate Revenue
- **Full Disclosure**: The App participates in affiliate programs including Amazon Associates, AliExpress, and others.
- **Commissions**: We earn a commission when users purchase products through links in the App.
- **No Additional Cost**: Commissions do not affect the price paid by the user.
- **Independence**: Our recommendations are not influenced by commission amounts.

### 6. Intellectual Property
- All content, design, and code in the App are protected by copyright.
- No copying, reproduction, or distribution of the App is permitted without written permission.
- Store brand names and logos are the property of their original owners.

### 7. Limitation of Liability
- **Indirect Damages**: We shall not be liable for any direct, indirect, incidental, or consequential damages arising from use or inability to use the App.
- **Purchase Decisions**: Users bear full responsibility for their purchase decisions.
- **Technical Issues**: We are not liable for malfunctions, service interruptions, or data loss.

---

**© 2026 Price Comparison App. All rights reserved.**
"""

PRIVACY_POLICY = """
# מדיניות פרטיות / Privacy Policy

**תאריך עדכון אחרון: 15 ינואר 2026 / Last Updated: January 15, 2026**

---

## עברית

### 1. מבוא
מדיניות פרטיות זו מסבירה כיצד אפליקציית השוואת המחירים אוספת, משתמשת ומגינה על המידע שלך.

### 2. מידע שאנו אוספים

#### 2.1 מידע שנשמר מקומית בלבד
- **היסטוריית חיפושים**: חיפושים שביצעת באפליקציה נשמרים **אך ורק במכשיר שלך**.
- **העדפות משתמש**: בחירות שפה, מצב תצוגה, והגדרות נשמרות מקומית בלבד.
- **אין שמירה בשרתים**: אנו **לא שומרים** את היסטוריית החיפושים בשרתים שלנו.

#### 2.2 מידע שאנו לא אוספים
- אנו **לא** אוספים מידע אישי מזהה (שם, כתובת, טלפון, אימייל).
- אנו **לא** עוקבים אחר הרגלי הגלישה שלך מחוץ לאפליקציה.
- אנו **לא** משתמשים ב-cookies למעקב.

### 3. שימוש במידע

#### 3.1 מטרות השימוש
- **שיפור חוויית משתמש**: היסטוריית החיפושים מאפשרת גישה מהירה לחיפושים קודמים.
- **תחזוקה טכנית**: מידע טכני אנונימי משמש לשיפור ביצועי האפליקציה.
- **אין שימוש מסחרי**: אנו **לא** מוכרים מידע אישי לצדדים שלישיים.

### 4. שיתוף מידע עם צדדים שלישיים

#### 4.1 קישורי שותפות
- כאשר אתה לוחץ על קישור לחנות חיצונית, **אתה עוזב את האפליקציה שלנו**.
- החנות החיצונית עשויה לאסוף מידע בהתאם למדיניות הפרטיות שלה.
- אנו **לא שולטים** במדיניות הפרטיות של אתרים חיצוניים.

### 5. אבטחת מידע
- **HTTPS**: כל התקשורת מוצפנת באמצעות HTTPS.
- **אחסון מקומי**: היסטוריה שמורה רק במכשיר שלך.
- **אין בסיס נתונים**: אין לנו בסיס נתונים שמכיל מידע אישי.

### 6. זכויות המשתמש
- **מחיקת מידע**: אתה יכול למחוק את היסטוריית החיפושים בכל עת.
- **גישה למידע**: יש לך גישה מלאה למידע השמור מקומית במכשיר שלך.

### 7. פרטיות ילדים
- האפליקציה אינה מיועדת לילדים מתחת לגיל 13.
- אנו לא אוספים מידע מילדים מתחת לגיל 13.

---

## ENGLISH

### 1. Introduction
This Privacy Policy explains how the Price Comparison Application collects, uses, and protects your information.

### 2. Information We Collect

#### 2.1 Information Stored Locally Only
- **Search History**: Searches are saved **only on your device**.
- **User Preferences**: Settings are stored locally only.
- **No Server Storage**: We do **not** save your data on our servers.

#### 2.2 Information We Do Not Collect
- We do **not** collect personally identifiable information.
- We do **not** track your browsing habits outside the App.
- We do **not** use tracking cookies.

### 3. Use of Information
- **Improving User Experience**: Search history allows quick access to previous searches.
- **Technical Maintenance**: Anonymous technical information improves App performance.
- **No Commercial Use**: We do **not** sell personal information.

### 4. Information Security
- **HTTPS**: All communication is encrypted.
- **Local Storage**: History stored only on your device.
- **No User Database**: No database containing personal information.

### 5. User Rights
- **Data Deletion**: You can delete search history at any time.
- **Access**: You have full access to locally stored information.

---

**© 2026 Price Comparison App. All rights reserved.**
"""

AFFILIATE_DISCLOSURE = """
# גילוי שותפות והצהרת אחריות / Affiliate Disclosure & Disclaimer

**תאריך עדכון אחרון: 15 ינואר 2026 / Last Updated: January 15, 2026**

---

## 📢 גילוי שותפות מלא / Full Affiliate Disclosure

### עברית

#### חשוב לדעת:
אפליקציית השוואת המחירים משתתפת בתוכניות שותפות עם חנויות ומוכרים שונים. **זה אומר שאנו מרוויחים עמלה כאשר אתה רוכש מוצר דרך הקישורים שלנו.**

#### 🔗 איך זה עובד?

**1. תוכניות השותפות שלנו:**
- **Amazon Associates** - תוכנית Amazon Services LLC Associates Program
- **AliExpress Affiliate Program** - תוכנית השותפות של AliExpress
- **תוכניות נוספות** - עשויות להתוסף חנויות נוספות

**2. מה קורה כשאתה קונה:**
- כאשר אתה לוחץ על קישור למוצר באפליקציה
- ורוכש מוצר באותו אתר
- אנו מקבלים עמלה קטנה מהחנות (בדרך כלל 1%-10%)

**3. האם זה עולה לך כסף נוסף?**
- **לא!** המחיר שאתה משלם זהה לחלוטין
- העמלה משולמת על ידי החנות, לא על ידיך
- אין עלויות נוספות או חיובים נסתרים

#### 💡 השפעה על ההמלצות

**אנו מתחייבים:**
- ✅ להציג מידע אובייקטיבי ומדויק על המחירים
- ✅ להשוות מחירים באופן הוגן בין כל החנויות
- ✅ שההמלצות שלנו לא מושפעות מגובה העמלות
- ✅ לציין בבירור כאשר קישור הוא קישור שותפות

---

## ⚠️ הצהרת אחריות / Disclaimer

### 1. דיוק המחירים
**חשוב מאוד:**
- המחירים המוצגים הם **אינדיקטיביים בלבד**
- המחירים עשויים להשתנות **בכל רגע**
- **תמיד** בדוק את המחיר הסופי באתר החנות
- אנו **לא אחראים** על הפרשי מחירים

### 2. זמינות מוצרים
- אין ערבות שהמוצר זמין למכירה
- המלאי עשוי להיגמר בכל עת
- **בדוק זמינות באתר החנות** לפני הרכישה

### 3. עלויות משלוח ומיסים
- המחירים **לא כוללים**:
  - עלויות משלוח
  - מסים (מע"ם, מכס)
  - עמלות נוספות
- העלות הסופית **עשויה להיות שונה**

### 4. החלטות רכישה
**אתה האחראי:**
- ✋ אנו מספקים כלי להשוואה בלבד
- ✋ אנו לא יועצים פיננסיים
- ✋ כל החלטת רכישה היא באחריותך
- ✋ השווה, חקור ובדוק לפני שאתה קונה

---

## ENGLISH

### 📢 Full Affiliate Disclosure

#### Important to Know:
The Price Comparison Application participates in affiliate programs with various stores. **This means we earn a commission when you purchase through our links.**

#### 🔗 How It Works

**1. Our Affiliate Programs:**
- **Amazon Associates**
- **AliExpress Affiliate Program**
- **Additional Programs**

**2. What Happens When You Buy:**
- When you click a product link in the App
- And purchase on that site
- We receive a small commission (typically 1%-10%)

**3. Does It Cost You Extra?**
- **No!** The price you pay is exactly the same
- Commission is paid by the store, not by you
- No additional costs or hidden charges

#### 💡 Impact on Recommendations

**We Commit To:**
- ✅ Present objective price information
- ✅ Compare prices fairly across all stores
- ✅ Recommendations not influenced by commissions
- ✅ Clearly indicate affiliate links

---

## ⚠️ Disclaimer

### 1. Price Accuracy
**Very Important:**
- Prices are **indicative only**
- Prices may change **at any moment**
- **Always** verify final price on store website
- We are **not responsible** for price differences

### 2. Product Availability
- No guarantee product is available
- Inventory may run out
- **Check availability on store website**

### 3. Shipping and Taxes
- Displayed prices **do not include**:
  - Shipping costs
  - Taxes (VAT, customs)
  - Additional fees
- Final cost **may be different**

### 4. Purchase Decisions
**You Are Responsible:**
- ✋ We provide comparison tools only
- ✋ We are not financial advisors
- ✋ All purchase decisions are your responsibility
- ✋ Compare, research, and verify before buying

---

**© 2026 Price Comparison App. All rights reserved.**
"""

# =====================================
# פונקציות עזר
# =====================================

def show_legal_page(doc_type):
    """מציג דף משפטי"""
    docs = {
        "terms": (TERMS_OF_SERVICE, "📋 תנאי שימוש / Terms of Service"),
        "privacy": (PRIVACY_POLICY, "🔒 מדיניות פרטיות / Privacy Policy"),
        "disclosure": (AFFILIATE_DISCLOSURE, "📢 גילוי שותפות / Affiliate Disclosure")
    }
    
    if doc_type in docs:
        content, title = docs[doc_type]
        
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
    
    /* הסתרת תפריט */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
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
            st.write("")
            st.write("")
            search_button = st.button("🔍 חפש / Search", use_container_width=True)
        
        if search_button and search_query:
            # שמירת חיפוש בהיסטוריה
            st.session_state.search_history.append({
                'query': search_query,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            
            st.success(f"✅ מחפש: {search_query}")
            
            # תוצאות
            st.markdown("---")
            st.subheader("📦 תוצאות / Results")
            
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
            
            # כפתורי קישור
            st.markdown("### 🛒 קישורים לרכישה / Purchase Links")
            cols = st.columns(len(stores))
            
            for idx, col in enumerate(cols):
                with col:
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
        
        # היסטוריה
        if st.session_state.search_history:
            with st.expander("📜 היסטוריית חיפושים / Search History"):
                for item in reversed(st.session_state.search_history[-10:]):
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
                
                st.success("🏆 העסקה הטובה ביותר / Best Deal: " + stores_list[0])
                
                st.dataframe(df_compare, use_container_width=True, hide_index=True)
                
                # גרף
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
                    st.info("💡 התקן plotly לגרפים: pip install plotly")
    
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
                st.metric("תשלום חודשי / Monthly Payment", f"${monthly_payment:.2f}")
            
            with col2:
                st.metric("סה\"כ לתשלום / Total Payment", f"${total_paid:.2f}")
            
            with col3:
                st.metric("סה\"כ ריבית / Total Interest", f"${total_interest:.2f}")
            
            with col4:
                st.metric("תוספת אחוזים / Percentage Added", f"{(total_interest/price)*100:.1f}%")
    
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
            
            valid_products = [p for p in products if p['name'] and p['price'] > 0]
            if valid_products:
                best = min(valid_products, key=lambda x: x['price'])
                st.success(f"🏆 המוצר הזול ביותר / Cheapest Product: {best['name']} - ${best['price']:.2f}")
    
    # ==================
    # טאב 5: קופונים
    # ==================
    with tab5:
        st.subheader("🎫 קופונים והנחות")
        
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
                "discount": "15% הנחה / 15% Off",
                "expiry": "28/02/2026",
                "link": "https://www.aliexpress.com"
            },
            {
                "store": "eBay",
                "code": "TECH10",
                "discount": "$10 הנחה / $10 Off",
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
