async function downloadVideo() {
    const urlInput = document.getElementById('videoUrl');
    const downloadBtn = document.getElementById('downloadBtn');
    const btnText = document.getElementById('btnText');
    const loader = document.getElementById('loader');
    const messageDiv = document.getElementById('message');

    const url = urlInput.value.trim();

    if (!url) {
        showMessage('Por favor ingresa una URL', 'error');
        return;
    }

    if (!url.includes('youtube.com') && !url.includes('youtu.be')) {
        showMessage('Por favor ingresa una URL válida de YouTube', 'error');
        return;
    }

    // Deshabilitar el botón y mostrar loader
    downloadBtn.disabled = true;
    btnText.classList.add('hidden');
    loader.classList.remove('hidden');
    messageDiv.classList.add('hidden');

    try {
        const response = await fetch('/download', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: url })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Error al descargar el video');
        }

        // Obtener el blob del video
        const blob = await response.blob();

        // Obtener el nombre del archivo del header
        const contentDisposition = response.headers.get('Content-Disposition');
        let filename = 'video.mp4';
        if (contentDisposition) {
            const filenameMatch = contentDisposition.match(/filename="?(.+)"?/);
            if (filenameMatch) {
                filename = filenameMatch[1];
            }
        }

        // Crear un link temporal y hacer clic en él para descargar
        const downloadUrl = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = downloadUrl;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(downloadUrl);
        a.remove();

        showMessage('¡Video descargado con éxito!', 'success');
        urlInput.value = '';

        // Limpiar archivos temporales en el servidor
        fetch('/cleanup', { method: 'POST' });

    } catch (error) {
        showMessage('Error: ' + error.message, 'error');
        console.error('Error:', error);
    } finally {
        // Restaurar el botón
        downloadBtn.disabled = false;
        btnText.classList.remove('hidden');
        loader.classList.add('hidden');
    }
}

function showMessage(text, type) {
    const messageDiv = document.getElementById('message');
    messageDiv.textContent = text;
    messageDiv.className = 'message ' + type;
    messageDiv.classList.remove('hidden');
}

// Permitir descargar con Enter
document.getElementById('videoUrl').addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        downloadVideo();
    }
});
