fetch("images_collection.json")
  .then(response => response.json())
  .then(images => {
    const gallery = document.getElementById("gallery");

    images.forEach(file => {
      const lastDot = file.lastIndexOf(".");
      let name = file;
      let ext = "";

      if (lastDot !== -1) {
        name = file.substring(0, lastDot);
        ext = file.substring(lastDot).toLowerCase();
      }

      const normalizedFile = name + ext;

      const container = document.createElement("div");
      container.classList.add("image-container");

      const label = document.createElement("div");
      label.classList.add("image-label");
      label.textContent = name;
      container.appendChild(label);

      const a = document.createElement("a");
      a.href = "images/" + encodeURIComponent(normalizedFile);
      a.target = "_blank";

      const img = document.createElement("img");
      img.src = "images/" + encodeURIComponent(normalizedFile);
      img.alt = name;

      a.appendChild(img);
      container.appendChild(a);

      gallery.appendChild(container);
    });
  })
  .catch(error => console.error("Error loading image list:", error));
