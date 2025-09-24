import React, {type ReactNode} from 'react';
import Translate from '@docusaurus/Translate';
import {ThemeClassNames} from '@docusaurus/theme-common';
import {useDateTimeFormat} from '@docusaurus/theme-common/internal';
import type {Props} from '@theme/LastUpdated';

function LastUpdatedAtDate({lastUpdatedAt}: {lastUpdatedAt: number}): ReactNode {
  const atDate = new Date(lastUpdatedAt);

  const dateTimeFormat = useDateTimeFormat({
    day: 'numeric',
    month: 'short',
    year: 'numeric',
  });

  const formattedLastUpdatedAt = dateTimeFormat.format(atDate);

  return (
    <Translate
      id="theme.lastUpdated.atDate"
      description="The words used to describe on which date a page has been last updated"
      values={{
        date: (
          <b>
            <time dateTime={atDate.toISOString()} itemProp="dateModified">
              {formattedLastUpdatedAt}
            </time>
          </b>
        ),
      }}>
      {' on {date}'}
    </Translate>
  );
}

function LastUpdatedByUser({lastUpdatedBy}: {lastUpdatedBy: string}): ReactNode {
  return (
    <Translate
      id="theme.lastUpdated.byUser"
      description="The words used to describe by who the page has been last updated"
      values={{
        user: <b>{lastUpdatedBy}</b>,
      }}>
      {' by {user}'}
    </Translate>
  );
}

export default function LastUpdated({lastUpdatedAt, lastUpdatedBy}: Props): ReactNode {
  const isDev = process.env.NODE_ENV === 'development';

  const resolvedLastUpdatedAt =
    typeof lastUpdatedAt === 'number'
      ? isDev
        ? Date.now()
        : lastUpdatedAt
      : undefined;

  const resolvedLastUpdatedBy =
    isDev && (!lastUpdatedBy || lastUpdatedBy === 'Author')
      ? undefined
      : lastUpdatedBy;

  return (
    <span className={ThemeClassNames.common.lastUpdated}>
      <Translate
        id="theme.lastUpdated.lastUpdatedAtBy"
        description="The sentence used to display when a page has been last updated, and by who"
        values={{
          atDate: resolvedLastUpdatedAt ? (
            <LastUpdatedAtDate lastUpdatedAt={resolvedLastUpdatedAt} />
          ) : (
            ''
          ),
          byUser: resolvedLastUpdatedBy ? (
            <LastUpdatedByUser lastUpdatedBy={resolvedLastUpdatedBy} />
          ) : (
            ''
          ),
        }}>
        {'Last updated{atDate}{byUser}'}
      </Translate>
    </span>
  );
}
