import type { ReactNode } from "react";
import { Check } from "lucide-react";

import { cn } from "@/lib/utils";

export function Section({
  id,
  alt,
  className,
  children,
}: {
  id?: string;
  alt?: boolean;
  className?: string;
  children: ReactNode;
}) {
  return (
    <section id={id} className={cn("px-4 py-14 sm:py-20", alt && "bg-surface", className)}>
      <div className="mx-auto w-full max-w-6xl">{children}</div>
    </section>
  );
}

export function Eyebrow({ children, className }: { children: ReactNode; className?: string }) {
  return (
    <p
      className={cn(
        "text-brand text-center text-xs font-semibold tracking-[0.25em] uppercase",
        className,
      )}
    >
      {children}
    </p>
  );
}

export function SectionTitle({ children, className }: { children: ReactNode; className?: string }) {
  return (
    <h2
      className={cn(
        "mt-3 text-center text-2xl font-extrabold tracking-tight sm:text-4xl",
        className,
      )}
    >
      {children}
    </h2>
  );
}

export function GradientButton({
  full,
  onClick,
  disabled,
  className,
  children,
}: {
  full?: boolean;
  onClick?: () => void;
  disabled?: boolean;
  className?: string;
  children: ReactNode;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      disabled={disabled}
      className={cn(
        "bg-brand shadow-glow text-primary-foreground inline-flex items-center justify-center gap-2 rounded-2xl px-6 py-4 text-sm font-semibold transition-transform duration-200 hover:scale-[1.02] disabled:pointer-events-none disabled:opacity-60",
        full && "w-full",
        className,
      )}
    >
      {children}
    </button>
  );
}

export function Pill({ children, className }: { children: ReactNode; className?: string }) {
  return (
    <span
      className={cn(
        "bg-brand text-primary-foreground inline-flex items-center gap-1.5 rounded-full px-4 py-1.5 text-xs font-semibold",
        className,
      )}
    >
      {children}
    </span>
  );
}

export function Card({ children, className }: { children: ReactNode; className?: string }) {
  return (
    <div
      className={cn(
        "shadow-soft border-border bg-card rounded-[20px] border p-6 sm:p-8",
        className,
      )}
    >
      {children}
    </div>
  );
}

export function Bullet({ children, className }: { children: ReactNode; className?: string }) {
  return (
    <li className={cn("flex items-start gap-3 text-sm leading-relaxed", className)}>
      <span className="bg-brand text-primary-foreground mt-0.5 inline-flex size-5 shrink-0 items-center justify-center rounded-full">
        <Check className="size-3" strokeWidth={3} aria-hidden />
      </span>
      <span>{children}</span>
    </li>
  );
}
