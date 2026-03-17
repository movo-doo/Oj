let allImages = [];
let activeCategory = null;

const gallery = document.getElementById("gallery");
const categoryBar = document.getElementById("category-bar");

// Load categories
fetch("json_categories.json")
  .then(res => res.json())
  .then(data => {
    data.categories.forEach(cat => {
      const btn = document.createElement("button");
      btn.innerHTML = cat.replace(" ", "<br>");
      btn.classList.add("category-button");

      btn.addEventListener("click", () => {
        activeCategory = cat;
        updateGallery();
        setActiveButton(btn);
      });

      categoryBar.appendChild(btn);
    });

    // Optional "All" button
    const allBtn = document.createElement("button");
    allBtn.textContent = "All";
    allBtn.classList.add("category-button", "active");

    allBtn.addEventListener("click", () => {
      activeCategory = null;
      updateGallery();
      setActiveButton(allBtn);
    });

    categoryBar.prepend(allBtn);
  });

// Load images
fetch("json_images.json")
  .then(res => res.json())
  .then(data => {
    allImages = data;
    updateGallery();
  });

// Update gallery display
function updateGallery() {
  gallery.innerHTML = "";

  const filtered = activeCategory
    ? allImages.filter(img => img.categories.includes(activeCategory))
    : allImages;

  filtered.forEach(item => {
    const file = item.file;

    const lastDot = file.lastIndexOf(".");
    let name = file.substring(0, lastDot);

    const container = document.createElement("div");
    container.classList.add("image-container");

    const label = document.createElement("div");
    label.classList.add("image-label");
    label.textContent = name;

    const a = document.createElement("a");
    a.href = "images/" + encodeURIComponent(file);
    a.target = "_blank";

    const img = document.createElement("img");
    img.src = "images/" + encodeURIComponent(file);
    img.alt = name;

    a.appendChild(img);
    container.appendChild(label);
    container.appendChild(a);
    gallery.appendChild(container);
  });
}

// Highlight active button
function setActiveButton(activeBtn) {
  document.querySelectorAll(".category-button").forEach(btn =>
    btn.classList.remove("active")
  );
  activeBtn.classList.add("active");
}
