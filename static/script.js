const container = document.querySelector('.container');
const registerBtn = document.querySelector('.register-btn');
const loginBtn = document.querySelector('.login-btn');


registerBtn.addEventListener('click', () => {
    container.classList.add('active');
})

loginBtn.addEventListener('click', () => {
    container.classList.remove('active');
})

function UpperWord(frase) {
    // Verifica que sea un string
    if (typeof frase !== 'string') {
      return '';
    }
    
    // Expresión regular para encontrar cada palabra
    // \b -> Límite de palabra
    // \w+ -> Una o más letras, dígitos o subrayados
    return frase.replace(/\b\w+/g, function (palabra) {
      return palabra.charAt(0).toUpperCase() + palabra.slice(1).toLowerCase();
    });
  }
  
document.addEventListener('DOMContentLoaded', function() {
    const userLogin = document.getElementById('userLogin');
    const userRegister = document.getElementById('userRegister');

    function UpperWord(string) {
        return string.replace(/\b\w/g, char => char.toUpperCase());
    }

    if (userLogin) {
        userLogin.addEventListener('input', function() {
            this.value = UpperWord(this.value);
        });
    }

    if (userRegister) {
        userRegister.addEventListener('input', function() {
            this.value = UpperWord(this.value);
        });
    }
});
  
