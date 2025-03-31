// Function to handle file selection and send the file to the backend
function handleFileSelect(event) {
  const file = event.target.files[0];
  if (!file) {
    alert("No file selected.");
    return;
  }

  // Check the file extension to ensure it's either CSV or Excel
  const fileName = file.name.toLowerCase();
  if (!(fileName.endsWith('.csv') || fileName.endsWith('.xlsx'))) {
    alert("Please select a valid CSV or Excel file.");
    return;
  }

  // Create a FormData object and append the file
  const formData = new FormData();
  formData.append('file', file);

  // Send the file to the backend endpoint using Fetch API
  fetch('/bulk_import', {
    method: 'POST',
    body: formData
  })
  .then(response => response.json())
  .then(result => {
    if (result.success) {
      alert("Bulk import successful. " + result.inserted + " new transactions added.");
      location.reload(); // Refresh the page to display updated data
    } else {
      alert("Bulk import failed: " + result.error);
    }
  })
  .catch(error => {
    console.error("Error during bulk import:", error);
    alert("Error during bulk import.");
  });
}
