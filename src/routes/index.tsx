import { createFileRoute } from "@tanstack/react-router";

import { LandingPage } from "@/components/landing/landing-page";

const TITLE = "[LOGO PRODUKTU] — [NAZWA PRODUKTU — odśnieżarka elektryczna 3000 W]";
const DESCRIPTION =
  "[META OPIS — obietnica efektu + główna przewaga + zachęta do kliknięcia, do 155 znaków]";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: TITLE },
      { name: "description", content: DESCRIPTION },
      { property: "og:title", content: TITLE },
      { property: "og:description", content: DESCRIPTION },
      { property: "og:type", content: "product" },
      { property: "og:image", content: "/images/hero.jpg" },
      { name: "twitter:card", content: "summary_large_image" },
    ],
  }),
  component: LandingPage,
});
