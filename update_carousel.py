import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

css_to_add = """
        /* Carousel CSS */
        .reviews-carousel {
            position: relative;
            max-width: 600px;
            margin: 0 auto;
            min-height: 200px;
        }
        .review-slide {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            opacity: 0;
            visibility: hidden;
            transition: opacity 0.8s ease-in-out, visibility 0.8s;
            z-index: 1;
        }
        .review-slide.active {
            opacity: 1;
            visibility: visible;
            z-index: 2;
            position: relative;
        }
"""

html = html.replace("</style>", css_to_add + "\n</style>")

# Replace the `<div class="grid-2"` inside reference with `<div class="reviews-carousel" id="reviewsCarousel">`
# and the review cards with `.review-slide`

# Find section
ref_start = html.find('<section id="reference">')
ref_end = html.find('</section>', ref_start) + len('</section>')

ref_section = html[ref_start:ref_end]

# We need to change:
# <div class="grid-2" style="max-width: 900px; margin: 0 auto;">
# to
# <div class="reviews-carousel" id="reviewsCarousel">
new_ref_section = ref_section.replace('<div class="grid-2" style="max-width: 900px; margin: 0 auto;">', '<div class="reviews-carousel" id="reviewsCarousel">')

# We need to add `review-slide` to the classes of the `a.review-card`
# First one should have `review-slide active`, second one `review-slide`
new_ref_section = new_ref_section.replace('class="review-card"', 'class="review-card review-slide active"', 1)
new_ref_section = new_ref_section.replace('class="review-card"', 'class="review-card review-slide"')

# Also add the script right before `</section>`
script_to_add = """
<script>
document.addEventListener("DOMContentLoaded", function() {
    const slides = document.querySelectorAll("#reviewsCarousel .review-slide");
    if(slides.length === 0) return;
    let currentSlide = 0;

    setInterval(() => {
        slides[currentSlide].classList.remove("active");
        currentSlide = (currentSlide + 1) % slides.length;
        slides[currentSlide].classList.add("active");
    }, 5000);
});
</script>
"""

new_ref_section = new_ref_section.replace('</section>', script_to_add + '</section>')

html = html[:ref_start] + new_ref_section + html[ref_end:]

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
print("Updated successfully")
