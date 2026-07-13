/**
 * ============================================================================
 * Landing Layout
 * ============================================================================
 *
 * Description:
 * Reusable landing page layout for VerdiGO.
 *
 * Author:
 * VerdiGO Frontend Team
 * ============================================================================
 */

import { ReactNode } from "react";

interface LayoutProps {
  children: ReactNode;
}

export default function DashboardLayout({ children }: LayoutProps) {
  return <>{children}</>;
}
