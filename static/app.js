// DOM elements
const form = document.getElementById("ideaForm")
const input = document.getElementById("idea")
const results = document.getElementById("results")
const resultsTitle = document.getElementById("resultsTitle")
const emptyState = document.getElementById("emptyState")
const generateBtn = document.getElementById("generateBtn")
const btnText = generateBtn.querySelector(".btn-text")
const loadingIcon = generateBtn.querySelector(".loading-icon")
const styleSelector = document.getElementById("styleSelector")
const selectedCountElement = document.getElementById("selectedCount")

// Domain pricing
const domainPricing = {
  ma: 120,
  com: 118,
  net: 150,
  org: 150,
  info: 180,
  me: 200,
  "net.ma": 140,
  "co.ma": 130,
  "press.ma": 160,
  "org.ma": 140,
  "gov.ma": 200,
  "ac.ma": 180,
}

// Function to get domain price
function getDomainPrice(domain) {
  const ext = extractExtension(domain)
  return domainPricing[ext] || 0
}

// Update selected extensions count
function updateSelectedCount() {
  const selectedCount = document.querySelectorAll('.extension-item input[type="checkbox"]:checked').length
  selectedCountElement.textContent = `${selectedCount} selected`
}

// Initialize on DOM load
document.addEventListener("DOMContentLoaded", () => {
  updateSelectedCount()

  // Handle extension item clicks
  document.querySelectorAll(".extension-item").forEach((item) => {
    const checkbox = item.querySelector('input[type="checkbox"]')

    item.addEventListener("click", (e) => {
      if (e.target !== checkbox) {
        checkbox.checked = !checkbox.checked
        item.classList.toggle("selected", checkbox.checked)
        updateSelectedCount()
      }
    })

    checkbox.addEventListener("change", () => {
      item.classList.toggle("selected", checkbox.checked)
      updateSelectedCount()
    })
  })
})

// Get selected extensions
function getSelectedExtensions() {
  return Array.from(document.querySelectorAll(".extension-item.selected")).map((item) => item.dataset.ext)
}

// Select All button
document.getElementById("selectAll").addEventListener("click", () => {
  document.querySelectorAll(".extension-item").forEach((item) => {
    const checkbox = item.querySelector('input[type="checkbox"]')
    checkbox.checked = true
    item.classList.add("selected")
  })
  updateSelectedCount()
})

// Deselect All button
document.getElementById("deselectAll").addEventListener("click", () => {
  document.querySelectorAll(".extension-item").forEach((item) => {
    const checkbox = item.querySelector('input[type="checkbox"]')
    checkbox.checked = false
    item.classList.remove("selected")
  })
  updateSelectedCount()
})

// Filter domains by selected extensions
function filterDomainsByExtensions(domains, selectedExts) {
  const allIndividualDomains = []

  domains.forEach((domainObj) => {
    const mainDomainExt = extractExtension(domainObj.domain)
    if (selectedExts.includes(mainDomainExt)) {
      allIndividualDomains.push({
        domain: domainObj.domain,
        status: domainObj.status,
        alt: [],
      })
    }

    domainObj.alt.forEach((altDomain) => {
      const altExt = extractExtension(altDomain)
      if (selectedExts.includes(altExt)) {
        allIndividualDomains.push({
          domain: altDomain,
          status: domainObj.status,
          alt: [],
        })
      }
    })
  })

  // Remove duplicates
  const uniqueDomains = allIndividualDomains.filter(
    (domain, index, self) => index === self.findIndex((d) => d.domain === domain.domain),
  )

  // Sort domains with .com and .ma first
  return uniqueDomains.sort((a, b) => {
    const aExt = extractExtension(a.domain)
    const bExt = extractExtension(b.domain)

    const getPriority = (ext) => {
      if (ext === "com") return 1
      if (ext === "ma") return 2
      return 3
    }

    const aPriority = getPriority(aExt)
    const bPriority = getPriority(bExt)

    return aPriority !== bPriority ? aPriority - bPriority : a.domain.localeCompare(b.domain)
  })
}

// Extract extension from domain
function extractExtension(domain) {
  const parts = domain.split(".")
  if (parts.length >= 3 && parts[parts.length - 1] === "ma") {
    return parts.slice(-2).join(".")
  }
  return parts[parts.length - 1]
}

// Create domain card
function createDomainCard(domain) {
  const price = getDomainPrice(domain.domain)

  const card = document.createElement("div")
  card.className = "domain-card"

  card.innerHTML = `
        <div class="domain-header">
            <div class="domain-name">${domain.domain}</div>
            <span class="domain-status status-${domain.status}">${domain.status}</span>
        </div>

        <div class="domain-pricing">
            <div class="domain-price">
                ${price.toFixed(2)} <span class="price-period">MAD/year</span>
            </div>
        </div>

        <div class="domain-actions">
            <button class="buy-btn" data-domain="${domain.domain}">
                <i class="fas fa-shopping-cart"></i>
                BUY NOW
            </button>
            <button class="action-btn copy-btn" title="Copy domain name">
                <i class="fas fa-copy"></i>
            </button>
        </div>
    `

  // Buy button event
  card.querySelector(".buy-btn").addEventListener("click", () => {
    const domainName = card.querySelector(".buy-btn").dataset.domain
    const url = `https://client.capconnect.com/cart.php?a=add&domain=register&query=${domainName}`
    window.open(url, "_blank")
  })

  // Copy button event
  card.querySelector(".copy-btn").addEventListener("click", async () => {
    try {
      await navigator.clipboard.writeText(domain.domain)
      const icon = card.querySelector(".copy-btn i")
      icon.className = "fas fa-check"
      setTimeout(() => { icon.className = "fas fa-copy" }, 1500)
    } catch (err) {
      alert(`Domain copied: ${domain.domain}`)
    }
  })

  return card
}

// Form submission
form.addEventListener("submit", async (e) => {
  e.preventDefault()

  const idea = input.value.trim()
  if (!idea) return

  const selectedExts = getSelectedExtensions()
  if (selectedExts.length === 0) {
    alert("Please select at least one domain extension.")
    return
  }

  const style = styleSelector.value

  // Show loading state
  btnText.style.display = "none"
  loadingIcon.style.display = "inline-block"
  generateBtn.disabled = true

  // Clear previous results
  results.innerHTML = ""
  resultsTitle.style.display = "none"
  emptyState.style.display = "none"

  try {
    const response = await fetch("/api/suggest", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        idea: idea,
        style: style,
        extensions: selectedExts
      })
    })

    if (!response.ok) throw new Error("Failed to generate domains")
    const data = await response.json()

    const filteredDomains = filterDomainsByExtensions(data, selectedExts)

    if (filteredDomains.length === 0) {
      results.innerHTML = `
        <div class="empty-state">
          <i class="fas fa-exclamation-circle"></i>
          <h3>No domains found</h3>
          <p>Try different extensions or another business idea</p>
        </div>
      `
    } else {
      resultsTitle.style.display = "block"
      filteredDomains.forEach((domain) => {
        results.appendChild(createDomainCard(domain))
      })
    }
  } catch (error) {
    console.error("Error:", error)
    results.innerHTML = `
      <div class="empty-state">
        <i class="fas fa-exclamation-triangle"></i>
        <h3>Failed to generate domains</h3>
        <p>Please try again later</p>
      </div>
    `
  } finally {
    btnText.style.display = "inline-block"
    loadingIcon.style.display = "none"
    generateBtn.disabled = false
  }
})