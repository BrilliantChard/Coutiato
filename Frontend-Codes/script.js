const form = document.getElementById("recommendation-form");
const steps = document.querySelectorAll(".form-step");
const stepBar = document.querySelectorAll(".step");
const nextBtn = document.getElementById("nextBtn");
const prevBtn = document.getElementById("prevBtn");
const summaryDiv = document.getElementById("summary");

let currentStep = 0;

function showStep(step) {
  steps.forEach((s, i) => {
    s.style.display = i === step ? "block" : "none";
    stepBar[i].classList.toggle("active", i === step);
  });
  prevBtn.style.display = step === 0 ? "none" : "inline-block";
  nextBtn.textContent = step === steps.length - 1 ? "💾 Get Course Recommendations" : "Next";
}

function validateStep(step) {
  const current = steps[step];
  const requiredFields = current.querySelectorAll("input[required], select[required]");

  for (let field of requiredFields) {
    if (!field.value.trim()) {
      alert("⚠️ Please fill all required fields.");
      return false;
    }
  }

  // Special validation for subjects
  if (step === 1) {
    const selectedSubjects = document.querySelectorAll('input[name="subjects"]:checked');
    if (selectedSubjects.length < 7 || selectedSubjects.length > 11) {
      alert("⚠️ Please select between 7 and 11 subjects.");
      return false;
    }
  }

  // Special validation for interests
  if (step === 2) {
    const selectedInterests = document.querySelectorAll('#interests option:checked');
    if (selectedInterests.length > 3) {
      alert("⚠️ Please select no more than 3 interests.");
      return false;
    }
  }

  return true;
}

function generateSummary() {
  const data = new FormData(form);
  const selectedSubjects = Array.from(document.querySelectorAll('input[name=\"subjects\"]:checked')).map(e => e.value);
  const selectedInterests = Array.from(document.querySelectorAll('#interests option:checked')).map(e => e.value);

  summaryDiv.innerHTML = `
    <h3>📄 Your Summary</h3>
    <p><strong>Name:</strong> ${data.get('name')}</p>
    <p><strong>Contact:</strong> ${data.get('contact')} | ${data.get('email')}</p>
    <p><strong>Location:</strong> ${data.get('constituency')}, ${data.get('county')} | Ethnicity: ${data.get('ethnicity')}</p>
    <p><strong>Cluster Points:</strong> ${data.get('cluster')}</p>
    <p><strong>Subjects:</strong> ${selectedSubjects.join(', ')}</p>
    <p><strong>Interests:</strong> ${selectedInterests.join(', ')}</p>
    <p><strong>Other:</strong> ${data.get('other-interest')}</p>
  `;
}

nextBtn.addEventListener("click", () => {
  if (currentStep < steps.length - 1) {
    if (!validateStep(currentStep)) return;
    currentStep++;
    showStep(currentStep);
    if (currentStep === steps.length - 1) generateSummary();
  } else {
    alert("🎉 Thank you! Your information has been submitted successfully!");
    form.reset();
    currentStep = 0;
    showStep(currentStep);
  }
});

prevBtn.addEventListener("click", () => {
  currentStep--;
  showStep(currentStep);
});

// Initial setup
showStep(currentStep);
