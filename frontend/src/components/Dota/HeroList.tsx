import { SimpleGrid, Box } from '@chakra-ui/react';
import { Hero } from '../../client/models';
import { HeroThumbnail } from './Thumbnail';



interface HeroListProps {
    heroes: Hero[];
}
  


export const HeroList = ({ heroes }: HeroListProps) => {
    return (
        <Box shadow="xs" p="4" mb="6">
            <SimpleGrid columns={[2, null, 3]} spacing="10px">
                {heroes?.map((hero) => {
                    // Print the value of hero to the console
                    console.log(hero);
                    return <HeroThumbnail key={hero.id} hero={hero} />;
                })}
            </SimpleGrid>
        </Box>
    );
};
export default HeroList