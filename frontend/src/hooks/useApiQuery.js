import { useCallback, useEffect, useState } from "react"
import { readableError } from "../services/api"

export function useApiQuery(load, dependencies = []) {
  const [state, setState] = useState({ loading: true, data: null, error: "" })
  const refresh = useCallback(async () => {
    setState((current) => ({ ...current, loading: true, error: "" }))
    try { setState({ loading: false, data: await load(), error: "" }) }
    catch (error) { setState({ loading: false, data: null, error: readableError(error) }) }
  }, dependencies)
  useEffect(() => { refresh() }, [refresh])
  return { ...state, refresh }
}
