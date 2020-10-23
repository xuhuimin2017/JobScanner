export function openInNewTab (link: string) {
  window.open(
    link,
    '_blank' // <- This is what makes it open in a new window.
  )
}
