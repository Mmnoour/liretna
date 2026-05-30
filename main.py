import streamlit as st

st.set_page_config(page_title="حاسبة الفكة السورية", page_icon="💵", layout="centered")

st.title("💵 حاسبة الفكة والمعاملات المالية")
st.subheader("احسب ميزانيتك بالعملتين واعرف الباقي بدقة")

st.markdown("---")

# 1. قسم المدخلات: ما يملكه المستخدم
st.header("1️⃣ الأموال التي معك حالياً:")
col1, col2 = st.columns(2)

with col1:
    user_new = st.number_input("المبلغ بالعملة الجديدة (ليرة):", min_value=0.0, step=10.0, value=0.0)
with col2:
    user_old = st.number_input("المبلغ بالعملة القديمة (ليرة):", min_value=0.0, step=500.0, value=0.0)

# 2. قسم سعر المنتج
st.header("2️⃣ تفاصيل الشراء:")
product_price_new = st.number_input("سعر المنتج بالعملة الجديدة (اتركها 0 إذا ستدخل السعر بالقديم):", min_value=0.0,
                                    step=10.0, value=0.0)
product_price_old = st.number_input("سعر المنتج بالعملة القديمة (اتركها 0 إذا أدخلت السعر بالجديد):", min_value=0.0,
                                    step=500.0, value=0.0)

st.markdown("---")

# زر الحساب والمنطق البرمجي
if st.button("احسب الباقي وعملية الدفع", use_container_width=True):

    # تحويل كل أموال المستخدم إلى القيمة الجديدة داخلياً للحساب
    # (كل 1000 قديم = 1 جديد)
    total_user_wallet_new = user_new + (user_old / 1000.0)

    # تحديد سعر المنتج الفعلي (سواء أدخله بالجديد أو القديم)
    if product_price_new > 0:
        actual_price_new = product_price_new
    else:
        actual_price_new = product_price_old / 1000.0

    # التحقق من كفاية الأموال
    if total_user_wallet_new < actual_price_new:
        st.error("❌ الأموال التي معك غير كافية لشراء هذا المنتج!")
    else:
        # حساب إجمالي الباقي بالعملة الجديدة
        total_change_new = total_user_wallet_new - actual_price_new

        # استخراج الفئات الصحيحة (أقل فئة جديدة هي 10 ليرات)
        # نقوم بقسمة الباقي على 10 لمعرفة كم ورقة من فئة الـ 10 (أو مضاعفاتها) يمكن إرجاعها جديد
        change_new_part = int(total_change_new // 10) * 10

        # الباقي من الكسور الصغير يتم تحويله وإرجاعه بالعملة القديمة
        remaining_fraction = total_change_new - change_new_part
        change_old_part = int(round(remaining_fraction * 1000))

        # عرض النتائج للمستخدم
        st.success("✅ تم الحساب بنجاح!")

        st.metric(label="إجمالي الباقي المقدر بالجديد", value=f"{total_change_new:,.2f} ليرة")

        st.markdown("### 📢 يجب على البائع إرجاع الباقي لك كالتالي:")

        if change_new_part > 0:
            st.info(f"💵 **بالعملة الجديدة:** {change_new_part:,} ليرة")
        if change_old_part > 0:
            st.warning(f"🪙 **بالعملة القديمة (الفكة والكسور):** {change_old_part:,} ليرة")

        if change_new_part == 0 and change_old_part == 0:
            st.info("المبلغ مدفوع بالتمام والكمال، لا يوجد باقي لك!")