import { Radio, RadioGroup, Stack } from "@chakra-ui/react";
import {SetHeroAttr} from '../../client/models'

interface HeroFilterByAttributeProps {
  setHeroAttr: SetHeroAttr;
}

export const HERO_ATTR = {
	STR: '0',
	AGI: '1',
	INT: '2',
    ALL: '3',
}

const DATA = [
  { label: "All", value: "" },
  { label: "Strength", value: HERO_ATTR.STR },
  { label: "Intelligence", value: HERO_ATTR.INT },
  { label: "Agility", value: HERO_ATTR.AGI }
];

export const HeroFilterByAttribute = ({
  setHeroAttr
}: HeroFilterByAttributeProps) => {
  return (
    <RadioGroup defaultValue="" onChange={setHeroAttr}>
      <Stack direction="row" spacing={4}>
        {DATA.map((option) => (
          <Radio key={option.value} value={option.value}>
            {option.label}
          </Radio>
        ))}
      </Stack>
    </RadioGroup>
  );
};
