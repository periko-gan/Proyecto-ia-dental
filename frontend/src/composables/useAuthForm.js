import { computed, ref, unref } from 'vue'
import { useRouter } from 'vue-router'
import { loginAndPersist, registerAndLogin } from '@/services/authService'

const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

export function useAuthForm(page) {
  const router = useRouter()

  const isLogin = computed(() => unref(page) === 'login')

  const fullName = ref('')
  const email = ref('')
  const password = ref('')
  const loading = ref(false)
  const errorMessage = ref('')
  const emailError = ref('')
  const passwordError = ref('')
  const emailTouched = ref(false)
  const passwordTouched = ref(false)
  const passwordVisible = ref(false)

  const formTitle = computed(() =>
    isLogin.value ? 'Bienvenido de nuevo' : 'Crea tu cuenta profesional',
  )
  const formSubtitle = computed(() =>
    isLogin.value
      ? 'Introduce tus credenciales para continuar.'
      : 'Proporciona tus credenciales clínicas para empezar.',
  )
  const submitLabel = computed(() => (isLogin.value ? 'Iniciar sesión' : 'Registrarse'))
  const submitLabelLoading = computed(() =>
    isLogin.value ? 'Iniciando sesión...' : 'Registrando...',
  )
  const switchText = computed(() =>
    isLogin.value ? 'No tienes una cuenta?' : 'Ya tienes una cuenta?',
  )
  const switchLabel = computed(() => (isLogin.value ? 'Registrate' : 'Inicia sesión'))
  const switchRouteName = computed(() => (isLogin.value ? 'Register' : 'Login'))

  function validateEmail() {
    const value = email.value.trim()

    if (!value) {
      emailError.value = 'Debes ingresar un correo electrónico.'
      return false
    }

    if (!EMAIL_REGEX.test(value)) {
      emailError.value = 'Ingresa un correo electrónico valido.'
      return false
    }

    emailError.value = ''
    return true
  }

  function validatePassword() {
    const value = password.value

    if (!value.trim()) {
      passwordError.value = 'Debes ingresar una contraseña.'
      return false
    }

    if (value.length < 8) {
      passwordError.value = 'La contraseña debe tener mínimo 8 caracteres.'
      return false
    }

    passwordError.value = ''
    return true
  }

  function validateFullName() {
    if (isLogin.value) {
      return true
    }

    const value = fullName.value.trim()
    if (!value) {
      errorMessage.value = 'Debes ingresar tu nombre completo.'
      return false
    }

    return true
  }

  function onEmailBlur() {
    emailTouched.value = true
    validateEmail()
  }

  function onPasswordBlur() {
    passwordTouched.value = true
    validatePassword()
  }

  function onEmailInput() {
    if (errorMessage.value) {
      errorMessage.value = ''
    }

    if (emailTouched.value) {
      validateEmail()
    }
  }

  function onPasswordInput() {
    if (errorMessage.value) {
      errorMessage.value = ''
    }

    if (passwordTouched.value) {
      validatePassword()
    }
  }

  function validateForm() {
    emailTouched.value = true
    passwordTouched.value = true
    const isFullNameValid = validateFullName()
    const isEmailValid = validateEmail()
    const isPasswordValid = validatePassword()
    return isFullNameValid && isEmailValid && isPasswordValid
  }

  function togglePasswordVisibility() {
    passwordVisible.value = !passwordVisible.value
  }

  async function handleSubmit() {
    errorMessage.value = ''

    if (!validateForm()) {
      return
    }

    const sanitizedEmail = email.value.trim()

    loading.value = true
    try {
      if (isLogin.value) {
        await loginAndPersist(sanitizedEmail, password.value)
      } else {
        await registerAndLogin(fullName.value.trim(), sanitizedEmail, password.value)
      }
      await router.push({ name: 'Dashboard' })
    } catch (error) {
      errorMessage.value = error?.message || 'No se pudo completar la operación.'
    } finally {
      loading.value = false
    }
  }

  return {
    isLogin,
    fullName,
    email,
    password,
    loading,
    errorMessage,
    emailError,
    passwordError,
    emailTouched,
    passwordTouched,
    passwordVisible,
    formTitle,
    formSubtitle,
    submitLabel,
    submitLabelLoading,
    switchText,
    switchLabel,
    switchRouteName,
    handleSubmit,
    onEmailBlur,
    onPasswordBlur,
    onEmailInput,
    onPasswordInput,
    togglePasswordVisibility,
  }
}
