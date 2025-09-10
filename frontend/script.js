document.addEventListener('DOMContentLoaded', () => {
    const imageUpload = document.getElementById('imageUpload');
    const imagePreview = document.getElementById('imagePreview');
    const previewImg = document.getElementById('previewImg');
    const submitButton = document.getElementById('submitButton');
    const plantInfo = document.getElementById('plantInfo');
    const plantDetails = document.getElementById('plantDetails');
    const chatbotSection = document.getElementById('chatbotSection');
    const chatbotMessages = document.getElementById('chatbotMessages');
    const chatbotInput = document.getElementById('chatbotInput');
    const sendButton = document.getElementById('sendButton');

    let uploadedImage = null;
    let identifiedPlant = null;

    // Handle drag and drop
    const dropZone = document.querySelector('label[for="imageUpload"]');

    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('bg-green-50');
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('bg-green-50');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('bg-green-50');
        const file = e.dataTransfer.files[0];
        if (file && file.type.startsWith('image/')) {
            handleImageFile(file);
        }
    });

    // Handle file input change
    imageUpload.addEventListener('change', (event) => {
        const file = event.target.files[0];
        if (file) {
            handleImageFile(file);
        }
    });

    function handleImageFile(file) {
        if (!file.type.startsWith('image/')) {
            alert('Please upload an image file.');
            return;
        }

        const reader = new FileReader();
        reader.onload = (e) => {
            previewImg.src = e.target.result;
            imagePreview.classList.remove('hidden');
            uploadedImage = file;
        };
        reader.readAsDataURL(file);
    }

    // Submit image for identification
    submitButton.addEventListener('click', async () => {
        if (!uploadedImage) {
            alert('Please upload an image first.');
            return;
        }

        submitButton.disabled = true;
        submitButton.innerHTML = 'Identifying...';

        const formData = new FormData();
        formData.append('file', uploadedImage);

        try {
           const response = await fetch('http://localhost:5000/predict', {
                method: 'POST',
                body: formData,
                credentials: 'include'  // Ensure session cookie is saved
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Failed to identify plant.');
            }

            if (data.error === 'invalid_plant') {
                alert('Please upload an image of one of the 5 supported flower types.');
                return;
            }

            identifiedPlant = data.name;
             console.log('Identified plant from predict:', identifiedPlant);
            // Display plant details
            plantDetails.innerHTML = `
                <p><strong>Common Name:</strong> ${data.name}</p>
                <p><strong>Scientific Name:</strong> ${data.info.scientific_name}</p>
                <p><strong>Growth Conditions:</strong> ${data.info.growth_conditions}</p>
                <p><strong>Description:</strong> ${data.info.description}</p>

            `;
            plantInfo.classList.remove('hidden');
            chatbotSection.classList.remove('hidden');
            chatbotMessages.innerHTML = `
                <div class="mb-2">
                    <p class="text-green-600"><strong>Bot:</strong> I've identified this plant as ${data.name}. Feel free to ask any questions about it!</p>
                </div>
            `;
        } catch (error) {
            alert(error.message || 'Error identifying plant.');
        } finally {
            submitButton.disabled = false;
            submitButton.innerHTML = 'Identify Plant';
        }
    });

    // Chatbot interaction
    sendButton.addEventListener('click', sendChatMessage);
    chatbotInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendChatMessage();
        }
    });

    async function sendChatMessage() {
        const query = chatbotInput.value.trim();
        if (!query) {
            return;
        }

        if (!identifiedPlant) {
            alert('Please identify a plant first before asking questions.');
            return;
        }

        chatbotInput.disabled = true;
        sendButton.disabled = true;

        try {
           const response = await fetch('http://localhost:5000/chatbot', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query }),
                credentials: 'include'
            });

            if (!response.ok) {
                throw new Error('Failed to get chatbot response.');
            }

            const data = await response.json();

            chatbotMessages.innerHTML += `
                <div class="mb-2">
                    <p class="text-gray-700"><strong>You:</strong> ${query}</p>
                    <p class="text-green-600"><strong>Bot:</strong> ${data.response}</p>
                </div>
            `;
            chatbotInput.value = '';
            chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
        } catch (error) {
            alert(error.message || 'Error getting chatbot response.');
        } finally {
            chatbotInput.disabled = false;
            sendButton.disabled = false;
        }
    }
});
