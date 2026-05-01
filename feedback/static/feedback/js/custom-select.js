/*
 * Custom Select — progressive enhancement.
 *
 * Replaces any <select class="js-custom-select"> with a fully styled,
 * keyboard-accessible dropdown. The original <select> stays in the DOM
 * (visually hidden) so Django form submission and validation are unchanged.
 *
 * Keyboard support:
 *   - Tab to focus the trigger.
 *   - Enter / Space / ArrowDown / ArrowUp opens the menu.
 *   - ArrowDown / ArrowUp navigates options.
 *   - Home / End jumps to first / last option.
 *   - Type-ahead (a-z, 0-9) jumps to the next matching option.
 *   - Enter / Space selects the highlighted option.
 *   - Escape closes the menu and returns focus to the trigger.
 *   - Click outside closes the menu.
 */
(function () {
    'use strict';

    function enhanceAll() {
        document.querySelectorAll('select.js-custom-select').forEach(enhance);
    }

    function enhance(selectEl) {
        if (selectEl.dataset.csEnhanced === 'true') return;
        selectEl.dataset.csEnhanced = 'true';

        var wrapper = document.createElement('div');
        wrapper.className = 'custom-select';
        wrapper.dataset.state = 'closed';

        var trigger = document.createElement('button');
        trigger.type = 'button';
        trigger.className = 'custom-select-trigger';
        trigger.setAttribute('aria-haspopup', 'listbox');
        trigger.setAttribute('aria-expanded', 'false');

        var labelEl = findLabelFor(selectEl);
        if (labelEl && labelEl.id) {
            trigger.setAttribute('aria-labelledby', labelEl.id);
        } else if (labelEl) {
            labelEl.id = labelEl.id || ('cs-label-' + cryptoRandom());
            trigger.setAttribute('aria-labelledby', labelEl.id);
        }

        var valueEl = document.createElement('span');
        valueEl.className = 'custom-select-value';
        trigger.appendChild(valueEl);

        var chevron = svg('chevron', 'm6 9 6 6 6-6');
        chevron.classList.add('custom-select-chevron');
        trigger.appendChild(chevron);

        var menu = document.createElement('ul');
        menu.className = 'custom-select-menu';
        menu.setAttribute('role', 'listbox');
        menu.tabIndex = -1;

        var optionEls = [];
        Array.prototype.forEach.call(selectEl.options, function (opt, idx) {
            var li = document.createElement('li');
            li.className = 'custom-select-option';
            li.setAttribute('role', 'option');
            li.dataset.value = opt.value;
            li.id = 'cs-opt-' + cryptoRandom() + '-' + idx;
            li.textContent = opt.textContent;
            if (opt.value === '') li.classList.add('is-placeholder');
            if (opt.disabled) {
                li.classList.add('is-disabled');
                li.setAttribute('aria-disabled', 'true');
            }
            li.addEventListener('mousedown', function (e) {
                e.preventDefault(); // keep focus on trigger
            });
            li.addEventListener('click', function () {
                if (opt.disabled) return;
                selectOption(idx);
                close(true);
            });
            li.addEventListener('mousemove', function () {
                if (highlighted !== idx) setHighlighted(idx);
            });
            menu.appendChild(li);
            optionEls.push(li);
        });

        // Move <select> into wrapper, place wrapper where the select was.
        var parent = selectEl.parentNode;
        parent.insertBefore(wrapper, selectEl);
        wrapper.appendChild(trigger);
        wrapper.appendChild(menu);
        wrapper.appendChild(selectEl);
        selectEl.classList.add('custom-select-native');
        selectEl.tabIndex = -1;
        selectEl.setAttribute('aria-hidden', 'true');

        var highlighted = Math.max(selectEl.selectedIndex, 0);
        var typeBuffer = '';
        var typeTimer = null;

        renderValue();
        setHighlighted(highlighted);

        // ----- helpers -----
        function renderValue() {
            var opt = selectEl.options[selectEl.selectedIndex];
            var placeholder = (selectEl.options[0] && selectEl.options[0].value === '')
                ? selectEl.options[0].textContent
                : 'Select an option';
            if (!opt || opt.value === '') {
                valueEl.textContent = placeholder;
                valueEl.classList.add('is-placeholder');
            } else {
                valueEl.textContent = opt.textContent;
                valueEl.classList.remove('is-placeholder');
            }
            optionEls.forEach(function (li, i) {
                li.classList.toggle('is-selected', i === selectEl.selectedIndex);
                li.setAttribute('aria-selected', i === selectEl.selectedIndex ? 'true' : 'false');
            });
        }

        function selectOption(idx) {
            if (idx < 0 || idx >= selectEl.options.length) return;
            selectEl.selectedIndex = idx;
            selectEl.dispatchEvent(new Event('input', { bubbles: true }));
            selectEl.dispatchEvent(new Event('change', { bubbles: true }));
            renderValue();
        }

        function setHighlighted(idx) {
            highlighted = clamp(idx, 0, optionEls.length - 1);
            optionEls.forEach(function (li, i) {
                li.classList.toggle('is-highlighted', i === highlighted);
            });
            var li = optionEls[highlighted];
            if (li) {
                trigger.setAttribute('aria-activedescendant', li.id);
                li.scrollIntoView({ block: 'nearest' });
            }
        }

        function open() {
            if (wrapper.dataset.state === 'open') return;
            wrapper.dataset.state = 'open';
            trigger.setAttribute('aria-expanded', 'true');
            setHighlighted(Math.max(selectEl.selectedIndex, 0));
            document.addEventListener('mousedown', onDocMouseDown, true);
            document.addEventListener('keydown', onMenuKey);
            window.addEventListener('resize', onViewportChange, { passive: true });
            window.addEventListener('scroll', onViewportChange, { passive: true });
            placeMenu();
        }

        function close(focusTrigger) {
            if (wrapper.dataset.state === 'closed') return;
            wrapper.dataset.state = 'closed';
            trigger.setAttribute('aria-expanded', 'false');
            trigger.removeAttribute('aria-activedescendant');
            document.removeEventListener('mousedown', onDocMouseDown, true);
            document.removeEventListener('keydown', onMenuKey);
            window.removeEventListener('resize', onViewportChange);
            window.removeEventListener('scroll', onViewportChange);
            menu.classList.remove('is-above');
            if (focusTrigger) trigger.focus();
        }

        function placeMenu() {
            // If there isn't enough space below, flip up.
            var rect = trigger.getBoundingClientRect();
            var spaceBelow = window.innerHeight - rect.bottom;
            var spaceAbove = rect.top;
            var menuHeight = menu.scrollHeight;
            if (spaceBelow < Math.min(menuHeight + 16, 240) && spaceAbove > spaceBelow) {
                menu.classList.add('is-above');
            } else {
                menu.classList.remove('is-above');
            }
        }

        function onViewportChange() {
            if (wrapper.dataset.state === 'open') placeMenu();
        }

        function onDocMouseDown(e) {
            if (!wrapper.contains(e.target)) close(false);
        }

        function onMenuKey(e) {
            switch (e.key) {
                case 'Escape':
                    e.preventDefault();
                    close(true);
                    break;
                case 'ArrowDown':
                    e.preventDefault();
                    setHighlighted(highlighted + 1);
                    break;
                case 'ArrowUp':
                    e.preventDefault();
                    setHighlighted(highlighted - 1);
                    break;
                case 'Home':
                    e.preventDefault();
                    setHighlighted(0);
                    break;
                case 'End':
                    e.preventDefault();
                    setHighlighted(optionEls.length - 1);
                    break;
                case 'Enter':
                case ' ':
                    e.preventDefault();
                    if (!selectEl.options[highlighted].disabled) {
                        selectOption(highlighted);
                        close(true);
                    }
                    break;
                case 'Tab':
                    close(false);
                    break;
                default:
                    if (e.key.length === 1 && !e.metaKey && !e.ctrlKey && !e.altKey) {
                        typeBuffer += e.key.toLowerCase();
                        if (typeTimer) clearTimeout(typeTimer);
                        typeTimer = setTimeout(function () { typeBuffer = ''; }, 600);
                        var start = highlighted + 1;
                        for (var offset = 0; offset < optionEls.length; offset++) {
                            var i = (start + offset) % optionEls.length;
                            var text = optionEls[i].textContent.toLowerCase().trim();
                            if (text.indexOf(typeBuffer) === 0) {
                                setHighlighted(i);
                                break;
                            }
                        }
                    }
            }
        }

        // Click toggles the menu.
        trigger.addEventListener('click', function (e) {
            e.preventDefault();
            if (wrapper.dataset.state === 'open') close(true);
            else open();
        });

        // When closed and trigger has focus, certain keys open the menu.
        trigger.addEventListener('keydown', function (e) {
            if (wrapper.dataset.state === 'open') return;
            if (['ArrowDown', 'ArrowUp', 'Enter', ' '].indexOf(e.key) !== -1) {
                e.preventDefault();
                open();
            }
        });

        // Reflect external changes (e.g. form reset, JS-driven updates).
        selectEl.addEventListener('change', function () {
            renderValue();
        });
    }

    function findLabelFor(el) {
        if (el.id) {
            var lbl = document.querySelector('label[for="' + el.id + '"]');
            if (lbl) return lbl;
        }
        var p = el.parentElement;
        while (p) {
            if (p.tagName === 'LABEL') return p;
            p = p.parentElement;
        }
        return null;
    }

    function clamp(n, min, max) {
        return Math.min(Math.max(n, min), max);
    }

    function cryptoRandom() {
        return Math.random().toString(36).slice(2, 9);
    }

    function svg(name, pathD) {
        var ns = 'http://www.w3.org/2000/svg';
        var s = document.createElementNS(ns, 'svg');
        s.setAttribute('viewBox', '0 0 24 24');
        s.setAttribute('width', '14');
        s.setAttribute('height', '14');
        s.setAttribute('fill', 'none');
        s.setAttribute('stroke', 'currentColor');
        s.setAttribute('stroke-width', '2.5');
        s.setAttribute('stroke-linecap', 'round');
        s.setAttribute('stroke-linejoin', 'round');
        s.setAttribute('aria-hidden', 'true');
        var p = document.createElementNS(ns, 'path');
        p.setAttribute('d', pathD);
        s.appendChild(p);
        return s;
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', enhanceAll);
    } else {
        enhanceAll();
    }
})();
