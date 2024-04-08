import { Hero } from "../../client/models";
import {Box, Image, Text, Flex} from "@chakra-ui/react";
interface HeroThumbnailProps {
    hero: Hero;
}


export const HeroThumbnail = ({ hero }: HeroThumbnailProps) => {

	const heroImgSrc = `/images/heroes/${hero.localized_name.toLocaleLowerCase().replace(/\ /g, '_')}.png`;
	const heroAttrImgSrc = `/images/icons/attr_${hero.primary_attr}.png`
	return (
		<Box>
        <Image width='225px' height='150px' src={heroImgSrc} alt={hero.localized_name} />
        <Text>
            <Flex justify='start' align='center' p='sm'>
                <Image src={heroAttrImgSrc} alt={`${hero.primary_attr}`} width='30px' height='30px' mr='sm' />
                <span>{hero.localized_name}</span>
            </Flex>
        </Text>
    </Box>
	)
}
export default HeroThumbnail

