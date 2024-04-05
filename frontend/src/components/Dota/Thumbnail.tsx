import { Hero } from "../../client/models";
import { Flex, Text, Box, Image} from "@chakra-ui/react";
interface HeroThumbnailProps {
    hero: Hero;
}


export const HeroThumbnail = ({ hero }: HeroThumbnailProps) => {

	const heroImgSrc = `https://cdn.cloudflare.steamstatic.com/apps/dota2/images/dota_react/heroes/${hero.name_loc.toLocaleLowerCase().replace(/\ /g, '_')}.png`
	const heroAttrImgSrc = `../assets/images/icons/attr_${hero.primary_attr}.png`

	return (
		<Box>
			<Image boxSize='100px' src={heroImgSrc} alt={hero.name_loc} />
			{/* <Text>
				<Flex justify='start' align='center' p='sm'>
					<Image src={heroAttrImgSrc} alt={`${hero.primary_attr}`}/>
					<span>{hero.name_loc}</span>
				</Flex>
			</Text> */}
		</Box>
	)
}
export default HeroThumbnail

