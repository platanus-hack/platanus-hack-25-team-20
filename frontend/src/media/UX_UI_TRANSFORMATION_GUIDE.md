# CV Tailor UX/UI Transformation Guide

This guide distills industry-leading patterns (Linear, Superhuman, Notion, Vercel, Stripe, Figma, Grammarly, Duolingo) into a concrete implementation plan for every part of the app. It is tailored to the current code structure (`frontend/src/pages/*`, `layouts/MainLayout.tsx`, shadcn/tailwind stack) and avoids generic styling.

---

## 1) Product Vision & References (map pattern → our feature)
- **Linear:** ultra-focused layouts, keyboard-first command palette, calm neutral surfaces with sharp accent gradients → apply to navigation, tables, and form density.
- **Superhuman:** triage workflows, fast keyboard shortcuts, contextual hover actions → apply to Submissions and Job cards.
- **Notion/Figma:** multi-modal input, inline editing, clear empty states, real-time collaboration feel → apply to Onboarding (upload/import/chat) and Editor.
- **Stripe/Vercel:** precise typography and expressive gradients for hero/CTA moments → apply to auth, top bars, and primary CTAs.
- **Grammarly/Notion AI:** AI chat affordances, quick prompt chips, diff previews → apply to the Editor and CV preview.
- **Duolingo/Headspace:** progress visualization and celebration → apply to onboarding success, submission milestones.

---

## 2) Design System Direction (tokens to wire into tailwind/theme)
- **Typography:** Headings with a modern grotesk (e.g., Space Grotesk or Sora), body with a clean sans (e.g., Inter variable or Geist). Set clear scale: 12/14/16/18/20/24/32/40/56 with 1.35–1.5 line-height.
- **Color System:** 
  - Base surfaces: `#0B1021` (dark), `#0F172A` (panel dark), `#FFFFFF` (light), `#F6F8FB` (muted light). 
  - Primary: electric blue `#2563FF` with gradient `from-[#2563FF] via-[#5B8CFF] to-[#7C3AED]`. 
  - Secondary accent: mint `#10B981` for success, amber `#F59E0B` for warnings, coral `#F97316` for AI activity. 
  - Borders: translucent `#E5E7EB` light, `#1F2937` dark.
- **Radii/Depth:** Use 14–16px radius for cards, 9999px pills for chips, subtle elevation (`shadow-[0_15px_50px_-24px_rgba(15,23,42,0.5)]`) and inner borders (`border border-white/6` on dark).
- **Motion:** 150–220ms ease-out for hover/focus; 300–450ms ease-in-out for modal/nav transitions. Use transform + opacity (no blur spam).
- **Grid/Spacing:** 12-col desktop grid; base spacing 8px; vertical rhythm 12–24px; keep max page width at 1200–1280px with generous gutters.
- **Copy Tone:** Concise, active, confidence-building. Pair CTAs with microcopy (what happens next).

---

## 3) Global UX Upgrades (apply across pages)
- **Top Bar + Left Nav:** Add compact top bar with search/command button, notifications, user menu, theme toggle. Refine left nav to a narrower rail, highlight active route with a pill + subtle glow.
- **Command Palette (⌘K / Ctrl+K):** Quick actions for "New application", "Upload CV", "Search jobs", "Jump to Editor", "Toggle theme". Reuse shadcn `Dialog` + searchable list.
- **Empty/Loading States:** Add skeletons for cards, list rows, and CV preview; empty states with icon, headline, and primary action. Use optimistic toasts with undo on destructive actions.
- **Toasts/Inline Feedback:** Standardize success/warn/error toasts; inline banners for blocking errors; progress bars for long AI/CV operations.
- **Search & Filters:** Persistent search bar with typeahead; filter chips for applied filters; "Save filter set" pattern on Jobs and Submissions.
- **Theming:** Keep light/dark parity; ensure gradients and borders adjust for both modes; add accessible focus rings (`outline-offset-2`, `ring-2 ring-primary/60`).

---

## 4) Feature-by-Feature Implementation Plan

### A) Authentication (Login/Signup)
- **Layout:** Two-column hero (pitch + logos/testimonial) and form card. Add "Why CV Tailor" bullets with icons and a mini preview image.
- **Form UX:** Inline validation with success ticks, password visibility toggle, strength meter, and "remember me". Add OAuth button states (loading/spinner).
- **Microcopy:** Below primary CTA, state next step: "Takes ~30 seconds to set up your profile."
- **Motion:** Slide-in form on load; subtle gradient shimmer on the hero background.

### B) Onboarding (Upload / Import / AI chat)
- **Step rail:** 3 steps with status (Current/Upcoming/Done) above tabs. Persist progress even if switching tabs.
- **Upload Path:** Drag-and-drop zone with file details + "Parse status" chip; show a 3-line parse preview; CTA "Continue" only enabled after parse success.
- **Import Path:** Pre-fill detection for GitHub/LinkedIn; show connection badges; add "Test fetch" inline feedback.
- **AI Chat Path:** Left chat stream, right live profile outline. Provide prompt chips ("Summarize last role", "Add quantifiable metrics"). Show typing indicator and streaming responses.
- **Success State:** Celebration check screen with confetti animation (CSS), showing "Profile strength" meter and CTA to Jobs.

### C) Dashboard (`Dashboard.tsx`)
- **Hero Panel:** Personalized greeting + "Next best action" pill (e.g., "Finish profile · 3 mins").
- **KPI Row:** Cards for Profile strength, Tailored CVs, Active applications, Win rate. Use mini progress bars/sparklines.
- **Timeline:** Recent activity feed (upload, AI edits, submissions) with icons and timestamps.
- **Skills & Gaps:** Two-column tags: strengths vs suggested skills to add; "Add to profile" quick action opens inline chip editor.
- **Empty State:** If no data, show "Start by uploading your CV" with direct CTA.

### D) Jobs List (`Jobs.tsx`)
- **Filters Panel:** Convert checkboxes to pill chips; add saved filter presets; show active filter bar with quick clear.
- **Job Card Layout:** Left: title/company; center: match score bar (AI) and top 3 keyword matches; right: primary CTA + quick save (bookmark) and "Open preview" icon. Hover reveals actions (save/share).
- **Density Controls:** Toggle between Comfortable and Compact list density.
- **Search:** Debounced search with inline loading bar; highlight matched terms.
- **Empty/Loading:** Card skeletons; empty state with "Adjust filters" + recommended filters chips.

### E) Job Detail (`JobDetail.tsx`)
- **Hero:** Gradient banner with job title, company logo placeholder, match score badge, and "Apply now" CTA. Add breadcrumb back to Jobs.
- **Highlights Bar:** Pill list for location, salary, seniority, visa/remote status.
- **Requirements Matrix:** Split into "You match" vs "Gaps" with progress indicators; suggest quick edits to cover gaps (links to Editor prompts).
- **CV Preview Panel:** Right column sticky card with larger preview, toggles for "Tailored" vs "Original", download/share buttons, and "Request AI improvement" mini prompt.
- **Interaction:** "Send to recruiter" CTA opens a confirmation dialog with email template preview.

### F) Editor (`Editor.tsx`)
- **Split View Enhancements:** Left chat, right live Typst render. Add tab switcher for "Diff" view (Before vs After) and "Sections" (jump to Education/Experience).
- **Prompt Chips:** Above textarea, chips for common edits ("Shorten summary", "Quantify impact", "Align to backend role").
- **System Messages:** Show AI typing indicator; show operation status bar when regenerating PDF; allow cancel.
- **Inline Annotations:** On rendered CV, hovering highlights corresponding chat message; clicking a section jumps to that context in chat.
- **Save/Versioning:** Add "Version history" dropdown (local list) to revert. Provide autosave indicator.
- **Submit Flow:** Confirmation modal with checklist (contact info present, skills added, no gaps).

### G) Submissions (`Submissions.tsx`)
- **View Toggle:** Table vs Kanban (columns: Draft, Submitted, Interview, Offer, Rejected). Drag-and-drop in Kanban updates status with optimistic UI.
- **Row Actions:** Hover to reveal "Open Job", "Download CV", "Send follow-up", "Add note".
- **Status Badges:** Harmonize badge colors; add tiny dots + tooltips for "updated X days ago".
- **Analytics Strip:** Above table, small charts for response rate and time-to-interview; filters for date range and status.
- **Empty State:** Showcase "Create first tailored CV" with steps and CTA.

### H) Settings (future-proof `MainLayout` link)
- Add a simple Settings skeleton page: profile info, notifications, theme, keyboard shortcuts reference.

---

## 5) Micro-Interactions & States
- **Hover/Focus:** Slight lift + shadow and border-glow on interactive cards/buttons; focus rings consistent across inputs and chips.
- **Transitions:** Page transitions fade+slide; modal scale-in; chip selection with background fade.
- **Feedback:** Toasts with optional undo for destructive actions; banners for blocking errors; inline field errors under inputs.
- **Skeletons:** Cards, table rows, chat bubbles, and Typst preview placeholder with shimmer.
- **Celebrations:** Confetti animation on successful onboarding or submission; subtle badge with "Streak" if multiple submissions in a week.

---

## 6) Accessibility & Responsiveness
- Maintain 16px base text, 44x44 tap targets, WCAG AA contrast for both themes.
- Keyboard: Tab order visible, Enter to submit, Esc to close dialogs, ⌘/Ctrl+K for command palette, arrow keys in lists.
- Responsive: 
  - Auth and onboarding center stack on mobile; background hero collapses to a gradient card.
  - Jobs/Submissions use stacked filters above results on mobile with collapsible accordion.
  - Editor: switch to vertical stack (chat above preview) with a toggle for "Preview only".

---

## 7) Phased Delivery Plan (execution order)
1) **Foundations:** Typography import, color tokens, radius/shadow utilities, global layout (top bar + nav), toasts, skeleton components. Ensure light/dark parity.
2) **High-Touch Flows:** Onboarding revamp (steps, parse previews), Jobs list/cards, Job detail hero+matrix, Editor chat/diff/prompt chips.
3) **Productivity Layer:** Command palette, keyboard shortcuts, save filters, density toggle, quick actions on cards.
4) **Operations & Insights:** Submissions Kanban/Table toggle, analytics strip, follow-up actions, dashboard KPI/timeline refresh.
5) **Polish & QA:** Motion tuning, empty/error states, accessibility sweep, cross-browser QA.

---

## 8) Implementation Notes by File
- `layouts/MainLayout.tsx`: Add top bar, slim nav rail, theme toggle, command palette trigger, user avatar menu. Update sidebar active styles and collapse-on-mobile behavior.
- `pages/Login.tsx` / `pages/Signup.tsx`: Two-column hero layout, inline validation, social proof, OAuth button states, password visibility toggle.
- `pages/Onboarding.tsx`: Add step rail, parse preview card, progress state, success celebration screen, prompt chips for chat tab, CTA hierarchy.
- `pages/Dashboard.tsx`: Replace static mock with KPI cards, timeline feed component, skills/gaps chips, "next action" spotlight card.
- `pages/Jobs.tsx`: Refactor filters to chips with save/clear, match score UI in cards, density toggle, search loading bar, empty state refresh.
- `pages/JobDetail.tsx`: Hero banner with match score, requirements matrix, CV preview controls (tailored vs original), quick prompt for improvements, apply modal.
- `pages/Editor.tsx`: Prompt chips, typing indicator, diff tab, section jump list, version history dropdown, operation status bar, submit checklist modal.
- `pages/Submissions.tsx`: View toggle (table/kanban), row hover actions, analytics strip, badge refresh, empty state.
- Components: Add `CommandPalette`, `StatusBadge`, `MatchScoreBar`, `Skeleton` variants, `Confetti` lightweight component, and reusable `PromptChips`.

---

## 9) Acceptance Criteria (what “done” looks like)
- All key flows (auth → onboarding → jobs → job detail → editor → submission) have clear primary CTA, progress cues, and helpful empty/loading/error states.
- Command palette works with keyboard; toasts and dialogs follow consistent style; light/dark parity verified.
- Jobs and Submissions support saved filters and density toggles; Job detail shows match score and CV controls.
- Editor supports prompt chips, typing indicator, and diff toggle; submit modal enforces checklist.
- Accessibility: focus rings present, keyboard navigation works, contrast passes AA, responsive layouts hold at common breakpoints.

---

## 10) Suggested Visual Moodboard (for reference)
- Neutral deep navy + soft light backgrounds with electric blue gradients for key CTAs.
- Rounded yet precise cards with inner borders and gentle glassiness on overlays.
- Clean grotesk headings, airy spacing, and purposeful icons. Minimal decoration; emphasize clarity and speed.
