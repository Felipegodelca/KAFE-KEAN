// ✅ main.js para KAFE KEAN

// 📌 Mensajes de Django
document.addEventListener('DOMContentLoaded', () => {
    console.log('✅ KAFE KEAN: JavaScript cargado correctamente.');

    const mensajes = document.querySelectorAll('.django-messages');
    mensajes.forEach(mensaje => {
        setTimeout(() => {
            mensaje.style.display = 'none';
        }, 5000);
    });

    // 📌 Botón para regresar arriba
    const btnArriba = document.createElement('button');
    btnArriba.innerText = '⬆️';
    btnArriba.className = 'btn-arriba';
    document.body.appendChild(btnArriba);

    btnArriba.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    window.addEventListener('scroll', () => {
        btnArriba.style.display = window.scrollY > 300 ? 'block' : 'none';
    });
});