/**
 * ============================================================================
 * Auth Layout
 * ============================================================================
 *
 * Description:
 * Reusable authentication layout for VerdiGO.
 *
 * Author:
 * VerdiGO Frontend Team
 * ============================================================================
 */

import { ReactNode } from "react";

interface LayoutProps {
  children: ReactNode;
}

export default function AuthLayout({ children }: LayoutProps) {
  return <>{children}</>;
}
