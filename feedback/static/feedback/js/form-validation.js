/*
 * Feedback form — required-field validation.
 *
 * Behaviour:
 *  - Intercepts submit; if any required field is empty, shows a toast,
 *    highlights every missing field's container with `.has-error`, and
 *    smooth-scrolls to the first one.
 *  - Listens for input / change events so highlighted fields lose their
 *    error state the moment the user fills them in.
 *  - Honours Django's server-rendered .has-error containers so the same
 *    toast fires on a page reload after a backend validation failure.
 */
(function () {
    'use strict';

    var TOAST_TIMEOUT_MS = 5000;

    function init() {
        document.querySelectorAll('form.feedback-form').forEach(setupForm);
        // Server-side errors: surface them in a toast on initial render.
        document.querySelectorAll('form.feedback-form').forEach(function (form) {
            var serverErrors = form.querySelectorAll('.has-error');
            if (serverErrors.length) {
                showToast(buildMessage(serverErrors.length));
                scrollIntoView(serverErrors[0]);
            }
        });
    }

    function setupForm(form) {
        form.addEventListener('submit', function (e) {
            var missing = collectMissing(form);
            if (missing.length) {
                e.preventDefault();
                clearErrors(form);
                missing.forEach(markField);
                triggerShake(missing[0]);
                showToast(buildMessage(missing.length));
                scrollIntoView(missing[0]);
            }
        });

        // Live clear-on-fix.
        form.addEventListener('input', function (e) {
            clearOwnerError(e.target);
        });
        form.addEventListener('change', function (e) {
            clearOwnerError(e.target);
        });
    }

    function collectMissing(form) {
        var missing = [];
        var seenGroups = new Set();

        // Text-style inputs / selects / textareas with `required`.
        form.querySelectorAll(
            'input[required], select[required], textarea[required]'
        ).forEach(function (el) {
            // Skip the (visually hidden) native select used by custom-select.js;
            // its trigger sits in .custom-select.
            if (el.classList.contains('custom-select-native')) {
                if (!el.value) missing.push(getFieldContainer(el));
                return;
            }
            var type = (el.type || '').toLowerCase();
            if (type === 'radio' || type === 'checkbox') {
                // Handled by the group sweep below.
                return;
            }
            if (!el.value || !el.value.trim()) {
                missing.push(getFieldContainer(el));
            }
        });

        // Radio groups: at least one option in the same name= must be checked.
        form.querySelectorAll('input[type="radio"]').forEach(function (radio) {
            if (!radio.required && !groupHasRequired(form, radio)) return;
            if (seenGroups.has(radio.name)) return;
            seenGroups.add(radio.name);
            var checked = form.querySelector(
                'input[type="radio"][name="' + cssEscape(radio.name) + '"]:checked'
            );
            if (!checked) {
                missing.push(getFieldContainer(radio));
            }
        });

        // Checkbox groups: Django's MultipleChoiceField (required=True) sets
        // each box's name= to e.g. "visit_reasons". We require at least one
        // checked when the group's container is rendered without a
        // server-supplied .is-optional hint.
        form.querySelectorAll('input[type="checkbox"]').forEach(function (cb) {
            if (seenGroups.has(cb.name)) return;
            seenGroups.add(cb.name);
            var container = getFieldContainer(cb);
            if (!container || container.dataset.optional === 'true') return;
            // Heuristic: only flag groups that live inside .choice-group
            // (single checkbox required fields are rare in this app).
            var inGroup = container.classList.contains('choice-group');
            if (!inGroup) return;
            var checked = form.querySelector(
                'input[type="checkbox"][name="' + cssEscape(cb.name) + '"]:checked'
            );
            if (!checked) {
                missing.push(container);
            }
        });

        return dedupe(missing).filter(Boolean);
    }

    function groupHasRequired(form, radio) {
        // True if any radio in the same name group has the required attribute.
        return !!form.querySelector(
            'input[type="radio"][name="' + cssEscape(radio.name) + '"][required]'
        );
    }

    function getFieldContainer(el) {
        return (
            el.closest('.field-group') ||
            el.closest('.choice-group') ||
            el.closest('.choice-card') ||
            el.parentElement
        );
    }

    function markField(container) {
        if (!container) return;
        container.classList.add('has-error');
    }

    function clearErrors(form) {
        form.querySelectorAll('.has-error').forEach(function (c) {
            c.classList.remove('has-error', 'is-shaking');
            // Also strip any inline error message we inserted.
            var inline = c.querySelector('.field-error[data-client="true"]');
            if (inline) inline.remove();
        });
    }

    function clearOwnerError(target) {
        if (!target) return;
        var c = getFieldContainer(target);
        if (c && c.classList.contains('has-error')) {
            c.classList.remove('has-error', 'is-shaking');
            var inline = c.querySelector('.field-error[data-client="true"]');
            if (inline) inline.remove();
        }
    }

    function triggerShake(container) {
        if (!container) return;
        container.classList.remove('is-shaking');
        // Force reflow so the animation restarts.
        // eslint-disable-next-line no-unused-expressions
        container.offsetWidth;
        container.classList.add('is-shaking');
    }

    function scrollIntoView(el) {
        if (!el) return;
        try {
            el.scrollIntoView({ behavior: 'smooth', block: 'center' });
        } catch (_) {
            el.scrollIntoView();
        }
        // After the smooth scroll, focus the first focusable element inside.
        setTimeout(function () {
            var focusable = el.querySelector(
                'input, select, textarea, button, [tabindex]:not([tabindex="-1"])'
            );
            if (focusable && typeof focusable.focus === 'function') {
                focusable.focus({ preventScroll: true });
            }
        }, 350);
    }

    function buildMessage(count) {
        if (count === 1) {
            return 'Please complete the highlighted field before submitting.';
        }
        return (
            'Please complete the ' + count + ' highlighted fields before submitting.'
        );
    }

    // ---------------- Toast ----------------

    var activeToast = null;
    var toastTimer = null;

    function showToast(message) {
        if (activeToast) {
            activeToast.remove();
            clearTimeout(toastTimer);
        }
        var toast = document.createElement('div');
        toast.className = 'form-toast form-toast--error';
        toast.setAttribute('role', 'alert');
        toast.setAttribute('aria-live', 'assertive');

        var icon = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
        icon.setAttribute('class', 'form-toast-icon');
        icon.setAttribute('viewBox', '0 0 24 24');
        icon.setAttribute('width', '20');
        icon.setAttribute('height', '20');
        icon.setAttribute('fill', 'none');
        icon.setAttribute('stroke', 'currentColor');
        icon.setAttribute('stroke-width', '2');
        icon.setAttribute('stroke-linecap', 'round');
        icon.setAttribute('stroke-linejoin', 'round');
        icon.setAttribute('aria-hidden', 'true');
        icon.innerHTML =
            '<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/>' +
            '<path d="M12 9v4"/><path d="M12 17h.01"/>';
        toast.appendChild(icon);

        var body = document.createElement('div');
        body.className = 'form-toast-body';
        body.textContent = message;
        toast.appendChild(body);

        var close = document.createElement('button');
        close.type = 'button';
        close.className = 'form-toast-close';
        close.setAttribute('aria-label', 'Dismiss notification');
        close.innerHTML =
            '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>';
        close.addEventListener('click', dismissToast);
        toast.appendChild(close);

        document.body.appendChild(toast);
        // Allow CSS transitions to pick up the entry state.
        requestAnimationFrame(function () {
            toast.classList.add('is-visible');
        });

        activeToast = toast;
        toastTimer = setTimeout(dismissToast, TOAST_TIMEOUT_MS);
    }

    function dismissToast() {
        if (!activeToast) return;
        var toast = activeToast;
        toast.classList.remove('is-visible');
        toast.classList.add('is-leaving');
        setTimeout(function () {
            if (toast.parentNode) toast.parentNode.removeChild(toast);
        }, 250);
        activeToast = null;
        clearTimeout(toastTimer);
    }

    // ---------------- Utilities ----------------

    function dedupe(list) {
        var out = [];
        var seen = new Set();
        list.forEach(function (item) {
            if (!seen.has(item)) {
                seen.add(item);
                out.push(item);
            }
        });
        return out;
    }

    function cssEscape(value) {
        if (window.CSS && typeof window.CSS.escape === 'function') {
            return window.CSS.escape(value);
        }
        return String(value).replace(/(["\\])/g, '\\$1');
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
