/**
 * ============================================================================
 * Dashboard Layout
 * ============================================================================
 *
 * Description:
 * Reusable dashboard layout for VerdiGO.
 *
 * Author:
 * VerdiGO Frontend Team
 * ============================================================================
 */

import { ReactNode } from "react";

interface LayoutProps {
  children: ReactNode;
}

export default function LandingLayout({ children }: LayoutProps) {
  return <>{children}</>;
}
