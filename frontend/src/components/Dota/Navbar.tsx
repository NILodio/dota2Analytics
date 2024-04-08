import { Flex, Text } from "@chakra-ui/react";

interface HeroToolbarProps {
    children: React.ReactNode;
}

export const HeroNavbar= ({ children }: HeroToolbarProps) => {
    return (
        <Flex
            as="nav"
            align="center"
            justify="space-between"
            wrap="wrap"
            padding="1.5rem"
            boxShadow="md"
        >
            <Text fontSize="md" fontWeight="bold" color="gray.700">
                Filter Hero
            </Text>
            {children}
        </Flex>
    );
};
export default HeroNavbar