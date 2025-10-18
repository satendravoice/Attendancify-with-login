// Matrix Rain Effect for Attendancify - Robust Implementation
// This script creates a fullscreen matrix code rain effect as background

function initMatrix() {
    // Check if we're on a page that should have the matrix effect
    const container = document.getElementById('matrix-background');
    if (!container) {
        console.log('Matrix background container not found');
        return;
    }

    // Configuration variables
    const CHARS = "アァカサタナハマヤャラワガザダバパイィキシチニヒミリヰギジヂビピウゥクスツヌフムユュルグズブヅプエェケセテネヘメレヱゲゼデベペオォコソトノホモヨョロヲゴゾドボポヴッン0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    const FONT_SIZE = 14;
    const MIN_SPEED = 3;
    const MAX_SPEED = 10;
    const MIN_FADE = 0.03;
    const MAX_FADE = 0.07;
    const DENSITY = 0.95; // Probability of character change (higher = more flickering)
    
    // Create canvas element if it doesn't exist
    let canvas = document.getElementById('matrix-canvas');
    if (!canvas) {
        canvas = document.createElement('canvas');
        canvas.id = 'matrix-canvas';
        container.appendChild(canvas);
    }
    
    // Set canvas dimensions to match window
    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    
    // Set initial font
    ctx.font = `${FONT_SIZE}px monospace`;
    ctx.textBaseline = 'top';
    
    // Create columns array
    const columns = [];
    const columnCount = Math.floor(canvas.width / FONT_SIZE);
    
    // Initialize columns
    for (let i = 0; i < columnCount; i++) {
        columns.push({
            x: i * FONT_SIZE,
            y: Math.random() * -canvas.height,
            speed: MIN_SPEED + Math.random() * (MAX_SPEED - MIN_SPEED),
            chars: [],
            fadeRate: MIN_FADE + Math.random() * (MAX_FADE - MIN_FADE),
            length: 5 + Math.floor(Math.random() * 20)
        });
        
        // Initialize characters for this column
        for (let j = 0; j < columns[i].length; j++) {
            columns[i].chars.push({
                char: CHARS.charAt(Math.floor(Math.random() * CHARS.length)),
                opacity: Math.random()
            });
        }
    }
    
    // Draw function
    function draw() {
        // Semi-transparent overlay to create fading effect - adjusted for better visibility
        ctx.fillStyle = 'rgba(18, 18, 18, 0.05)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        // Set text style
        ctx.font = `${FONT_SIZE}px monospace`;
        
        // Draw each column
        columns.forEach(column => {
            // Update column position
            column.y += column.speed;
            
            // Reset column if it goes well off screen (with buffer)
            if (column.y - column.length * FONT_SIZE > canvas.height + 200) {
                column.y = Math.random() * -200;
                column.speed = MIN_SPEED + Math.random() * (MAX_SPEED - MIN_SPEED);
                column.length = 5 + Math.floor(Math.random() * 20);
                
                // Reinitialize characters for this column
                column.chars = [];
                for (let j = 0; j < column.length; j++) {
                    column.chars.push({
                        char: CHARS.charAt(Math.floor(Math.random() * CHARS.length)),
                        opacity: Math.random()
                    });
                }
            }
            
            // Draw each character in the column
            for (let i = 0; i < column.length; i++) {
                const yPos = column.y - i * FONT_SIZE;
                
                // Only draw if character is on screen (with buffer)
                if (yPos > -200 && yPos < canvas.height + 100) {
                    // Randomly change character
                    if (Math.random() > DENSITY) {
                        column.chars[i].char = CHARS.charAt(Math.floor(Math.random() * CHARS.length));
                    }
                    
                    // Fade trail effect - head is brightest
                    const headOpacity = 0.8; // Reduced opacity for better visibility
                    const trailOpacity = Math.max(0, 1 - (i / column.length));
                    column.chars[i].opacity = i === 0 ? headOpacity : trailOpacity * 0.5; // Reduced trail opacity
                    
                    // Set color based on position in trail (Spotify green with enhanced visibility)
                    if (i === 0) {
                        // Head character - bright Spotify green with enhanced visibility
                        ctx.fillStyle = `rgba(29, 185, 84, ${Math.min(0.9, column.chars[i].opacity * 1.2)})`;
                    } else if (i < 3) {
                        // Near head - lighter Spotify green with enhanced visibility
                        ctx.fillStyle = `rgba(29, 185, 84, ${Math.min(0.7, column.chars[i].opacity * 0.9)})`;
                    } else {
                        // Trail - darker Spotify green with enhanced visibility
                        ctx.fillStyle = `rgba(29, 185, 84, ${Math.min(0.5, column.chars[i].opacity * 0.6)})`;
                    }
                    
                    // Draw character
                    ctx.fillText(column.chars[i].char, column.x, yPos);
                }
            }
        });
        
        // Continue animation loop
        requestAnimationFrame(draw);
    }
    
    // Start animation
    draw();
    
    // Handle window resize
    window.addEventListener('resize', () => {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    });
    
    // Handle theme changes (matrix visible in both modes but with different intensity)
    function updateVisibility() {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        if (currentTheme === 'dark') {
            container.style.opacity = '0.4';
        } else {
            container.style.opacity = '0.2';
        }
    }
    
    // Initial visibility check
    updateVisibility();
    
    // Watch for theme changes
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === 'attributes' && mutation.attributeName === 'data-theme') {
                updateVisibility();
            }
        });
    });
    
    observer.observe(document.documentElement, {
        attributes: true
    });
    
    // Ensure matrix effect is visible on all pages
    container.style.display = 'block';
}

// Initialize matrix effect when DOM is loaded
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initMatrix);
} else {
    // DOM is already loaded
    initMatrix();
}

// Also initialize when page is fully loaded
window.addEventListener('load', initMatrix);