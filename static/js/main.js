// 确保网页的 HTML 结构全都加载完了再执行 JS
document.addEventListener('DOMContentLoaded', function() {

    // 获取注册表单和输入框
    const signupForm = document.querySelector('#signupSection form');
    const signupPassword = document.getElementById('signupPassword');
    const confirmPassword = document.getElementById('confirmPassword');

    // 如果当前页面有注册表单，才执行后续逻辑
    if (signupForm) {

        // 1. 密码强度实时检测 (Password strength indicator)
        signupPassword.addEventListener('input', function() {
            const val = this.value;
            // 简单的强度判断逻辑：长度大于8，且包含数字
            if (val.length === 0) {
                this.className = 'form-control'; // 恢复原样
            } else if (val.length < 8 || !/\d/.test(val)) {
                this.className = 'form-control is-invalid'; // Bootstrap的红框报错样式
            } else {
                this.className = 'form-control is-valid'; // Bootstrap的绿框通过样式
            }
        });

        // 2. 两次密码一致性实时检测
        confirmPassword.addEventListener('input', function() {
            if (this.value === '') {
                this.className = 'form-control';
            } else if (this.value !== signupPassword.value) {
                this.className = 'form-control is-invalid';
            } else {
                this.className = 'form-control is-valid';
            }
        });

        // 3. 拦截表单提交，进行最终验证并“模拟测试”
        signupForm.addEventListener('submit', function(e) {
            // 【核心魔法】阻止表单的默认跳转和刷新行为！
            e.preventDefault();

            // 清除之前的旧错误提示
            document.querySelectorAll('.custom-error').forEach(el => el.remove());

            let isValid = true;
            const emailInput = document.getElementById('signupEmail');
            const nameInput = document.getElementById('signupName');

            // 检查姓名是否为空
            if (!nameInput.value.trim()) {
                showError(nameInput, 'Please enter your full name.');
                isValid = false;
            }

            // 检查密码是否通过
            if (!signupPassword.classList.contains('is-valid')) {
                showError(signupPassword, 'Password must be at least 8 characters and contain a number.');
                isValid = false;
            }

            // 检查两次密码是否一致
            if (signupPassword.value !== confirmPassword.value) {
                showError(confirmPassword, 'Passwords do not match.');
                isValid = false;
            }

            // 如果全部通过，模拟发送给后端
            if (isValid) {
                // 把按钮文字变成“加载中”，模拟网络延迟
                const submitBtn = signupForm.querySelector('button[type="submit"]');
                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = 'CREATING ACCOUNT...';
                submitBtn.disabled = true;

                // 模拟一个 1.5 秒的后端处理时间 (这里就是你现在的测试方法)
                setTimeout(() => {
                    alert('前端测试成功！数据校验完美。等后端接口写好，这里替换成真实的 fetch 请求即可。');

                    // 恢复按钮状态
                    submitBtn.innerHTML = originalText;
                    submitBtn.disabled = false;
                    // signupForm.reset(); // 可以重置表单
                }, 1500);
            }
        });
    }

    // 辅助函数：在输入框下方插入红色的错误提示文字 (Error messages display below invalid fields)
    function showError(inputElement, message) {
        inputElement.classList.add('is-invalid');
        const errorDiv = document.createElement('div');
        errorDiv.className = 'invalid-feedback custom-error d-block small mt-1';
        errorDiv.innerText = message;
        inputElement.parentNode.appendChild(errorDiv);
    }

    // === 密码可见性切换 (小眼睛功能) ===
    const togglePasswordButtons = document.querySelectorAll('.toggle-password');

    togglePasswordButtons.forEach(button => {
        button.addEventListener('click', function() {
            // 找到与这个按钮紧挨着的输入框
            const passwordInput = this.previousElementSibling;

            // 切换输入框的类型
            if (passwordInput.type === 'password') {
                passwordInput.type = 'text';
                this.innerHTML = '👁️';
            } else {
                passwordInput.type = 'password';
                this.innerHTML = '🙈';
            }
        });
    });
});