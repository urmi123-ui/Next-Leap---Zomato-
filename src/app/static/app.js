// Initialize Lucide Icons
document.addEventListener('DOMContentLoaded', () => {
    if (window.lucide) {
        window.lucide.createIcons();
    }
    initApp();
});

// State
let locations = [];
let cuisines = [];

// DOM Elements
const locationSelect = document.getElementById('location');
const cuisineSelect = document.getElementById('cuisine');
const minRatingSlider = document.getElementById('min-rating');
const minRatingVal = document.getElementById('rating-val');
const topKSlider = document.getElementById('top-k');
const topKVal = document.getElementById('top-k-val');
const prefsForm = document.getElementById('preferences-form');
const loaderSection = document.getElementById('loader');
const loaderMessage = document.getElementById('loader-message');
const resultsSection = document.getElementById('results');
const resultsCount = document.getElementById('results-count');
const aiSummaryText = document.getElementById('ai-summary-text');
const recommendationsGrid = document.getElementById('recommendations-grid');
const emptyState = document.getElementById('empty-state');
const submitBtn = document.getElementById('submit-btn');

// Image Map function mimicking Python server helper
function getRestaurantImage(cuisines, name) {
    const cuisinesLower = cuisines.map(c => c.toLowerCase());
    const nameLower = name.toLowerCase();

    if (cuisinesLower.some(c => c.includes('biryani')) || nameLower.includes('biryani')) {
        return "https://lh3.googleusercontent.com/aida-public/AB6AXuC4bGymiW8kqdTxzu3T_CU9pu7D5gqIF0Cgq5S-TpxF5xurvukJ_LU0Kav4IEAcKi55sHsVaB3O9IzjJgNW5g4iwXYwcv3grpYz3bC320qzkI2GE-Jg6IwOuYmFyNfevogdHszsOXxgcZ86KBW7KXVf2cUX8bbculcnPSCrN1RkbBS4Tm16vo4_FMlIk4u7yDPhYECqv6cekKdEWuMHyqgBqo3WlyBa96FCpQNdl-_lO47VsOOCxyye";
    }
    if (cuisinesLower.some(c => c.includes('south indian')) || nameLower.includes('andhra') || nameLower.includes('dosa')) {
        return "https://lh3.googleusercontent.com/aida-public/AB6AXuD9b5EwnilJ8TyfeyjcCXv0vSqPUVL0TMrSS3U0YH7biyOi8fOeRc1yKUjjyRM8lhsv0abCUp55p0R7evnMYtipcGligDWDR9_WXWtz-KQvjHvRYBw1Ea5C8TcRoU2JRuTRJkMQjJ6vP1UwhWA4-7n6-Md5dz-JGVv2kmOecsfe5dtmiRnP-QD4LjuKQ2MSBOIeIiUbVIG_yCkJnK2wjSeZqB4rWmjPwxMOEeBlOFIaGRJj98RmibS3";
    }
    if (cuisinesLower.some(c => ['ramen', 'japanese', 'korean', 'thai'].some(x => c.includes(x)))) {
        return "https://lh3.googleusercontent.com/aida-public/AB6AXuDAHHh2mRlfVHjTTnjuZEz1ih6F2G7aXv5EoLT-i9bOFyZ-jrpPxs3mvJqNwRZnJO796PUXZ4KTco3REtpCztmr5EkCaGIbAVcERLuVc93cV0W5zu-6MvigU5HhfVqHlDf9WDOqdfbeHE8Fb3dbP34w9wpo121AWyG_4t4WO-4vCRlUmq4JFvDwKfHnd_slXIW3GFVIs8HD3VmqFMfruxK67TKtu4JxLR7fZDiBMNYl_U1o_gkt9wbY";
    }
    if (cuisinesLower.some(c => ['chinese', 'asian', 'continental'].some(x => c.includes(x)))) {
        return "https://lh3.googleusercontent.com/aida-public/AB6AXuAhKPs_zhJ09ZTiWmgLNNgFJMRa0Cmcl5pchdPAs4ibjQKZwm2hjRQeF6DvGNMLv3dTy8AAx0lqVdSqUh451EPu7TQDsm4Pc78uFl18bEiiQuENUtOZ-OJ8iivTupB5iBvqgyregy50z37Mt6-3fiblf4595KGyI1M7gfZVLPlmc3m2G99uuwI0q7wurpLcRknw0I7Dq_hErpccyQdH7B5xtzfm_xHugK_Ny2rEnL-a-zUSv2JrfZVA";
    }
    if (cuisinesLower.some(c => ['italian', 'pizza', 'pasta'].some(x => c.includes(x)))) {
        return "https://images.unsplash.com/photo-1513104890138-7c749659a591?auto=format&fit=crop&q=80&w=600";
    }
    if (cuisinesLower.some(c => ['cafe', 'coffee', 'desserts', 'fast food', 'burger'].some(x => c.includes(x)))) {
        return "https://images.unsplash.com/photo-1498804103079-a6351b050096?auto=format&fit=crop&q=80&w=600";
    }
    return "https://lh3.googleusercontent.com/aida-public/AB6AXuDvw3j7rQQ6gG4_yZ_bvSwA3JbTA5B0dN6Va-xHiu2MbUZsBsD6Pa3xfYXynZx-BcZ99O4hUV7rUs9FImjGSXi5Q3b4xJYJMdetQjeK0EmkJaU6aljUL7_xikWWExZnsXoQY-einT_ahqKgCIb2balfs19c5lH4uZznyIgpikdueTeUbqeHewsonede6gPw2QRWjgr3eRMzH_CkrE9S9C07tw8BodCz1bn9ebx6Miqh2XFZ95aam-WR";
}

// Initial Loading & Event Setup
async function initApp() {
    // Dynamic sliders labels
    minRatingSlider.addEventListener('input', (e) => {
        minRatingVal.textContent = parseFloat(e.target.value).toFixed(1);
    });

    topKSlider.addEventListener('input', (e) => {
        topKVal.textContent = e.target.value;
    });

    // Populate selectors
    await fetchMetadata();

    // Form submission
    prefsForm.addEventListener('submit', handleFormSubmit);
}

// Fetch lists from Backend
async function fetchMetadata() {
    try {
        const [locRes, cuisRes] = await Promise.all([
            fetch('/api/v1/metadata/locations'),
            fetch('/api/v1/metadata/cuisines')
        ]);

        if (locRes.ok) {
            locations = await locRes.json();
            populateDropdown(locationSelect, locations, "Banashankari");
        } else {
            console.error("Failed to load locations");
            useFallbackLocations();
        }

        if (cuisRes.ok) {
            cuisines = await cuisRes.json();
            populateDropdown(cuisineSelect, cuisines, "North Indian");
        } else {
            console.error("Failed to load cuisines");
            useFallbackCuisines();
        }
    } catch (err) {
        console.error("Error connecting to backend API: ", err);
        useFallbackLocations();
        useFallbackCuisines();
    }
}

function useFallbackLocations() {
    locations = ["Banashankari", "Jayanagar", "JP Nagar", "Indiranagar", "Koramangala",
                 "Whitefield", "HSR Layout", "BTM Layout", "Marathahalli", "Electronic City"];
    populateDropdown(locationSelect, locations, "Banashankari");
}

function useFallbackCuisines() {
    cuisines = ["North Indian", "South Indian", "Chinese", "Continental", "Italian",
                "Mughlai", "Biryani", "Street Food", "Cafe", "Desserts"];
    populateDropdown(cuisineSelect, cuisines, "North Indian");
}

function populateDropdown(selectElement, list, defaultValue) {
    // Keep first placeholder
    const placeholder = selectElement.options[0];
    selectElement.innerHTML = '';
    selectElement.appendChild(placeholder);

    list.forEach(item => {
        const option = document.createElement('option');
        option.value = item;
        option.textContent = item;
        if (item === defaultValue) {
            option.selected = true;
        }
        selectElement.appendChild(option);
    });
}

// Submitting Preferences
async function handleFormSubmit(e) {
    e.preventDefault();

    const selectedLocation = locationSelect.value;
    const selectedCuisine = cuisineSelect.value;
    const minRating = parseFloat(minRatingSlider.value);
    const topK = parseInt(topKSlider.value);
    const additional = document.getElementById('additional-preferences').value.trim();
    
    // Budget Band
    const budgetElement = document.querySelector('input[name="budget"]:checked');
    const budget = budgetElement ? budgetElement.value : 'medium';

    // Show loading
    showLoading(true);

    const payload = {
        location: selectedLocation,
        budget: budget,
        cuisine: selectedCuisine,
        min_rating: minRating,
        additional_preferences: additional || null,
        top_k: topK
    };

    try {
        const res = await fetch('/api/v1/recommendations', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        if (!res.ok) {
            throw new Error(`API returned HTTP ${res.status}: ${await res.text()}`);
        }

        const data = await res.json();
        renderResults(data);
    } catch (err) {
        showError(err.message);
    } finally {
        showLoading(false);
    }
}

// Loader State Manager
const loadingMessages = [
    "Zomato AI is scanning Bangalore restaurants...",
    "Querying structured ratings and budget data...",
    "Injecting candidates into Llama 3.1 model...",
    "Formulating personalized reasoning explanations...",
    "Garnishing recommendations with premium visual style..."
];

let loaderInterval = null;

function showLoading(isLoading) {
    if (isLoading) {
        loaderSection.classList.remove('hidden');
        resultsSection.classList.add('hidden');
        emptyState.classList.add('hidden');
        submitBtn.disabled = true;
        submitBtn.style.opacity = '0.6';
        
        let msgIndex = 0;
        loaderMessage.textContent = loadingMessages[msgIndex];
        
        loaderInterval = setInterval(() => {
            msgIndex = (msgIndex + 1) % loadingMessages.length;
            loaderMessage.textContent = loadingMessages[msgIndex];
        }, 3000);
    } else {
        clearInterval(loaderInterval);
        loaderSection.classList.add('hidden');
        submitBtn.disabled = false;
        submitBtn.style.opacity = '1';
    }
}

// Rendering Results
function renderResults(data) {
    recommendationsGrid.innerHTML = '';
    
    if (!data.recommendations || data.recommendations.length === 0) {
        // Show empty results
        emptyState.classList.remove('hidden');
        emptyState.querySelector('h3').textContent = 'No matching spots found';
        emptyState.querySelector('p').textContent = 'Try adjusting your location, cuisine filters, or lowering minimum rating.';
        resultsSection.classList.add('hidden');
        return;
    }

    resultsSection.classList.remove('hidden');
    resultsCount.textContent = `${data.recommendations.length} option${data.recommendations.length !== 1 ? 's' : ''} curated`;
    
    // AI Summary
    if (data.summary) {
        aiSummaryText.textContent = `"${data.summary.replace(/^"|"$/g, '')}"`;
        document.querySelector('.ai-summary-card').classList.remove('hidden');
    } else {
        document.querySelector('.ai-summary-card').classList.add('hidden');
    }

    // Rank class & icons
    const rankBadges = {
        1: { class: 'rank-gold', icon: '🥇' },
        2: { class: 'rank-silver', icon: '🥈' },
        3: { class: 'rank-bronze', icon: '🥉' }
    };

    // Split: first card is Hero Layout, rest are Secondary Grid
    const firstRec = data.recommendations[0];
    const heroCard = createRestaurantCard(firstRec, true, rankBadges[1] || { class: 'rank-other', icon: '' });
    recommendationsGrid.appendChild(heroCard);

    if (data.recommendations.length > 1) {
        const secondaryContainer = document.createElement('div');
        secondaryContainer.className = 'secondary-grid';
        
        for (let i = 1; i < data.recommendations.length; i++) {
            const rec = data.recommendations[i];
            const badge = rankBadges[rec.rank] || { class: 'rank-other', icon: '' };
            const card = createRestaurantCard(rec, false, badge);
            secondaryContainer.appendChild(card);
        }
        
        recommendationsGrid.appendChild(secondaryContainer);
    }

    // Trigger icon creation for newly added cards
    if (window.lucide) {
        window.lucide.createIcons();
    }
}

function createRestaurantCard(rec, isHero, badgeInfo) {
    const r = rec.restaurant;
    const imgUrl = getRestaurantImage(r.cuisines, r.name);
    
    const card = document.createElement('div');
    card.className = `rest-card ${isHero ? 'hero-layout' : ''}`;
    
    // Tags HTML
    const tagsHTML = r.cuisines.slice(0, isHero ? 4 : 3)
        .map(tag => `<span class="cuisine-tag">${tag}</span>`)
        .join('');

    const costTwo = r.estimated_cost ? `₹${Math.round(r.estimated_cost)} for two` : `${r.budget_band.toUpperCase()} budget`;
    
    card.innerHTML = `
        <div class="rest-img-wrapper">
            <div class="rank-badge ${badgeInfo.class}">${badgeInfo.icon} #${rec.rank}</div>
            ${isHero ? '<div class="featured-tag">⚡ Top Pick</div>' : ''}
            <img class="rest-img" src="${imgUrl}" alt="${r.name}" loading="lazy">
            <div class="rest-img-overlay"></div>
        </div>
        <div class="rest-info-wrapper">
            <h3 class="rest-title">${r.name}</h3>
            <div class="rest-meta">
                <span class="rating-badge">
                    <i data-lucide="star"></i> ${r.rating ? r.rating.toFixed(1) : 'New'}
                </span>
                <span class="rest-loc">
                    <i data-lucide="map-pin"></i> ${r.location}
                </span>
                <span class="rest-cost">
                    <i data-lucide="indian-rupee"></i> ${costTwo}
                </span>
            </div>
            <div class="rest-tags">
                ${tagsHTML}
            </div>
            <div class="ai-why-card">
                <div class="ai-why-title">✦ Why Zomato AI Curated This</div>
                <div class="ai-why-desc">"${rec.explanation.replace(/^"|"$/g, '')}"</div>
            </div>
        </div>
    `;
    
    return card;
}

// Error state display
function showError(message) {
    resultsSection.classList.remove('hidden');
    resultsCount.textContent = `0 options`;
    
    // Overwrite recommendations grid with error layout
    recommendationsGrid.innerHTML = `
        <div class="empty-state-card" style="margin: 0 auto; border-color: rgba(226, 55, 68, 0.3); background: rgba(226, 55, 68, 0.02);">
            <div class="empty-icon-container" style="background: rgba(226, 55, 68, 0.08); border-color: rgba(226, 55, 68, 0.2);">
                <i data-lucide="alert-triangle" style="color: var(--primary-color);"></i>
            </div>
            <h3 style="color: white;">Connection / API Error</h3>
            <p style="margin-top: 10px;">${message}</p>
            <p style="font-size: 11px; margin-top: 20px; color: var(--text-muted);">Make sure the backend FastAPI service is running and configured correctly.</p>
        </div>
    `;
    
    // Hide AI Summary
    document.querySelector('.ai-summary-card').classList.add('hidden');
    
    if (window.lucide) {
        window.lucide.createIcons();
    }
}
