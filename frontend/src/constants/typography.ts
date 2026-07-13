/**
 * ============================================================================
 * VerdiGO Design System - Typography
 * ============================================================================
 *
 * Description:
 * Centralized typography tokens for the entire application.
 *
 * Module:
 * Phase 1 → Module 2 → Task 2
 *
 * Author:
 * VerdiGO Frontend Team
 * ============================================================================
 */

export const TYPOGRAPHY = {
    fontFamily: {
        sans: "Inter, sans-serif",
        mono: "monospace",
    },

    fontWeight: {
        light: 300,
        normal: 400,
        medium: 500,
        semibold: 600,
        bold: 700,
        extrabold: 800,
    },

    h1: {
        fontSize: "48px",
        fontWeight: 700,
        lineHeight: "56px",
    },

    h2: {
        fontSize: "40px",
        fontWeight: 700,
        lineHeight: "48px",
    },

    h3: {
        fontSize: "32px",
        fontWeight: 600,
        lineHeight: "40px",
    },

    h4: {
        fontSize: "28px",
        fontWeight: 600,
        lineHeight: "36px",
    },

    h5: {
        fontSize: "24px",
        fontWeight: 600,
        lineHeight: "32px",
    },

    h6: {
        fontSize: "20px",
        fontWeight: 600,
        lineHeight: "28px",
    },

    bodyLarge: {
        fontSize: "18px",
        lineHeight: "28px",
    },

    body: {
        fontSize: "16px",
        lineHeight: "24px",
    },

    bodySmall: {
        fontSize: "14px",
        lineHeight: "20px",
    },

    caption: {
        fontSize: "12px",
        lineHeight: "16px",
    },

    label: {
        fontSize: "14px",
        fontWeight: 500,
        lineHeight: "20px",
    },
} as const;