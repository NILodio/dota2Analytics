import { useMemo, useState } from 'react'

import { Hero } from '../../client/models'

export const useFilteredHeroes = (heroes: Hero[]) => {
	const [heroFilter, setHeroFilter] = useState('')

	const filteredHeroes = useMemo(() => {
		return heroes?.filter((hero: Hero) =>
			hero.localized_name.toLocaleLowerCase().includes(heroFilter.toLocaleLowerCase()),
		)
	}, [heroFilter, heroes])

	return { filteredHeroes, heroFilter, setHeroFilter }
}

export default useFilteredHeroes