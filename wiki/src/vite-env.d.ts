/// <reference types="vite/client" />
declare module 'virtual:kamaen-registry' {
  const registry: import('./world/types').Registry;
  export default registry;
}
