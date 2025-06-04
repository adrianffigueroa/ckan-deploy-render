document.addEventListener('DOMContentLoaded', function () {
  const titleSelect = document.querySelector('select[name="title"]');
  const nameInput = document.querySelector('input[name="name"]');
  const urlLabel = document.querySelector('label[for="field-name"]');

  if (!titleSelect || !nameInput || !urlLabel) return;

  // Ocultar el input pero no el grupo completo
  nameInput.style.display = 'none';

  // Crear el elemento de preview
  const preview = document.createElement('div');
  preview.className = 'url-preview';
  preview.style.margin = '6px 0 12px 0';
  preview.style.fontSize = '14px';
  preview.style.color = '#666';

  // Insertar debajo del label "URL"
  urlLabel.insertAdjacentElement('afterend', preview);

  function slugify(text) {
    return text
      .toString()
      .normalize("NFD").replace(/[\u0300-\u036f]/g, "")
      .toLowerCase()
      .trim()
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/^-+|-+$/g, '');
  }

  function updateSlug() {
    const selectedText = titleSelect.options[titleSelect.selectedIndex].text;
    const slug = slugify(selectedText);
    nameInput.value = slug;
    preview.innerHTML = `🔗 <strong>URL del grupo:</strong> <code>http://localhost:5000/group/${slug}</code>`;
  }

  updateSlug();
  titleSelect.addEventListener('change', updateSlug);
});
