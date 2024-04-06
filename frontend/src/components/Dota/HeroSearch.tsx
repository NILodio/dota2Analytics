import { Input } from '@chakra-ui/react'
import {SetHeroFilter} from '../../client/models'

interface HeroSearchProps {
	setHeroFilter: SetHeroFilter
}

export const HeroSearch = ({ setHeroFilter }: HeroSearchProps) => {
	return (
		<Input placeholder='Search hero' onChange={(event) => setHeroFilter(event.currentTarget.value)} />
	)
}