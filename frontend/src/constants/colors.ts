/**
 * ============================================================================
 * VerdiGO Design System - Color Palette
 * ============================================================================
 *
 * Description:
 * Centralized color tokens used across the application.
 * Avoid hardcoding colors inside components.
 *
 * Module:
 * Phase 1 → Module 2 → Task 1
 *
 * Author:
 * VerdiGO Frontend Team
 * ============================================================================
 */

export const COLORS = {
    // Primary Brand
    primary: "#16A34A",
    primaryDark: "#15803D",
    primaryLight: "#4ADE80",

    // Secondary
    secondary: "#2563EB",
    secondaryDark: "#1D4ED8",
    secondaryLight: "#60A5FA",

    // Accent
    accent: "#F59E0B",

    // Status
    success: "#22C55E",
    warning: "#FACC15",
    error: "#EF4444",
    info: "#3B82F6",

    // Text
    textPrimary: "#111827",
    textSecondary: "#6B7280",
    textMuted: "#9CA3AF",

    // Background
    background: "#FFFFFF",
    backgroundSecondary: "#F9FAFB",
    backgroundMuted: "#F3F4F6",

    // Border
    border: "#E5E7EB",

    // Neutral Scale
    white: "#FFFFFF",
    black: "#000000",

    gray50: "#F9FAFB",
    gray100: "#F3F4F6",
    gray200: "#E5E7EB",
    gray300: "#D1D5DB",
    gray400: "#9CA3AF",
    gray500: "#6B7280",
    gray600: "#4B5563",
    gray700: "#374151",
    gray800: "#1F2937",
    gray900: "#111827",
} as const;