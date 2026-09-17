import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useRef,
  useState,
  type ReactNode,
} from "react";
type SignalState = {
  seen: string[];
  frequency: number;
  motion: boolean;
  revision: number;
  observe: (id: string) => void;
  setFrequency: (value: number) => void;
  setMotion: (value: boolean) => void;
  clear: () => void;
};
const Context = createContext<SignalState>({
  seen: [],
  frequency: 0.6,
  motion: true,
  revision: 0,
  observe: () => {},
  setFrequency: () => {},
  setMotion: () => {},
  clear: () => {},
});
const key = "kamaen-observation-v1";
function read() {
  try {
    const v = JSON.parse(localStorage.getItem(key) || "null");
    return {
      seen: Array.isArray(v?.seen)
        ? [
            ...new Set<string>(
              v.seen.filter((s: unknown) => typeof s === "string"),
            ),
          ].slice(0, 2000)
        : [],
      frequency:
        typeof v?.frequency === "number" && Number.isFinite(v.frequency)
          ? Math.max(0.2, Math.min(1.6, v.frequency))
          : 0.6,
      motion: v?.motion !== false,
    };
  } catch {
    return { seen: [], frequency: 0.6, motion: true };
  }
}
export function SignalProvider({ children }: { children: ReactNode }) {
  const [state, setState] = useState(read),
    [revision, setRevision] = useState(0);
  const last = useRef("");
  useEffect(() => {
    const root = document.documentElement;
    root.style.setProperty("--signal-period", `${1 / state.frequency}s`);
    root.dataset.motion = state.motion ? "active" : "paused";
    try {
      localStorage.setItem(key, JSON.stringify(state));
    } catch {}
  }, [state]);
  const observe = useCallback((id: string) => {
    if (!id) return;
    setState((s) =>
      s.seen.includes(id) ? s : { ...s, seen: [...s.seen, id].slice(-2000) },
    );
    if (last.current !== id) {
      last.current = id;
      setRevision((r) => r + 1);
    }
  }, []);
  return (
    <Context.Provider
      value={{
        ...state,
        revision,
        observe,
        setFrequency: (frequency) =>
          setState((s) => ({
            ...s,
            frequency: Math.max(0.2, Math.min(1.6, frequency)),
          })),
        setMotion: (motion) => setState((s) => ({ ...s, motion })),
        clear: () => {
          last.current = "";
          setState((s) => ({ ...s, seen: [] }));
          setRevision(0);
        },
      }}
    >
      {children}
    </Context.Provider>
  );
}
export const useSignal = () => useContext(Context);
